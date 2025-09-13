from decimal import Decimal
from uuid import UUID, uuid4
from sqlalchemy import Date, Result, cast, exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

from app.infrastructure.repositories.transaction_repositories__sqlalchemy import SQLAlchemyTransactionRepository
from app.models.recurring_transaction import RecurringTransaction
from app.models.recurring_transaction_history import RecurringTransactionHistory
from app.models.transaction import Transaction

from ...schemas.transaction_schema import RecurringFrequency
from ...infrastructure.repositories.user_repositories__sqlalchemy import SQLAlchemyUserRepository

class SQLAlchemyRecurringTransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = SQLAlchemyUserRepository(db)
        self.transaction_repo = SQLAlchemyTransactionRepository(db)
    
    def _calculate_next_due_date_from_now(self, frequency: RecurringFrequency) -> datetime:
        """Calculate the next due date based on frequency from now."""
        return self._calculate_next_due_date_from_date(datetime.now(timezone.utc), frequency)
    
    def _calculate_next_due_date_from_date(self, from_date: datetime, frequency: str) -> datetime:
        """Calculate the next due date based on frequency from a specific date."""
        # Ensure we're working with timezone-aware datetime
        if from_date.tzinfo is None:
            from_date = from_date.replace(tzinfo=timezone.utc)
            
        if frequency == RecurringFrequency.daily:
            return from_date + timedelta(days=1)
        elif frequency == RecurringFrequency.weekly:
            return from_date + timedelta(weeks=1)
        elif frequency == RecurringFrequency.monthly:
            # Handle month rollover properly
            if from_date.month == 12:
                return from_date.replace(year=from_date.year + 1, month=1)
            else:
                return from_date.replace(month=from_date.month + 1)
        elif frequency == RecurringFrequency.yearly:
            return from_date.replace(year=from_date.year + 1)
        else:
            raise ValueError(f"Unsupported frequency: {frequency}")

    async def add_user_recurring_transaction(
        self, 
        transaction_name: str, 
        transaction_amount: Decimal, 
        currency_code: str,
        user_id: UUID,
        category_id: UUID,
        frequency: RecurringFrequency,
        next_due_date: datetime | None
    ):  
        try:
            create_immediate_transaction = next_due_date is None
            
            if create_immediate_transaction:
                calculated_due_date = self._calculate_next_due_date_from_now(frequency)
            else:
                calculated_due_date = next_due_date

            recurring_transaction = RecurringTransaction(
                name=transaction_name,
                amount=transaction_amount,
                currency_id=currency_code,
                user_id=user_id,
                category_id=category_id,
                frequency=frequency,
                next_due_date=calculated_due_date
            )

            self.db.add(recurring_transaction)
            await self.db.flush()  
            
            if create_immediate_transaction:
                immediate_transaction = Transaction(
                    name=transaction_name,
                    amount=transaction_amount,
                    currency_id=currency_code,
                    user_id=user_id,
                    category_id=category_id,
                )
                self.db.add(immediate_transaction)
                await self.db.flush()  

                category_type = await self.transaction_repo.get_category_type(category_id)
                await self.user_repo.update_user_balance(category_type, transaction_amount, user_id)

                transaction_history = RecurringTransactionHistory(
                    recurring_transaction_id=recurring_transaction.id
                )
                self.db.add(transaction_history) 

            await self.db.commit()
            return recurring_transaction
        except Exception as e:
            await self.db.rollback()
            raise ValueError(f"Failed to process recurring transaction: {str(e)}") from e
        

    async def check_recurring_transaction_history(self, recurring_transaction_id: UUID, target_date: datetime):
        """Check if a recurring transaction has already been triggered for a specific date."""
        query = exists().where(
            RecurringTransactionHistory.recurring_transaction_id == recurring_transaction_id,
            cast(RecurringTransactionHistory.triggered_at, Date) == cast(target_date, Date)
        )
        result: Result = await self.db.execute(query)
        return result.scalar()

    async def check_recurring_transaction(self, user_id: UUID):
        """Check and process all due recurring transactions for a user."""
        user_recurring_transactions_result = await self.db.execute(
            select(RecurringTransaction)
            .where(
                RecurringTransaction.user_id==user_id,
                RecurringTransaction.next_due_date <= datetime.now(timezone.utc)
            )
        )

        user_recurring_transactions = user_recurring_transactions_result.scalars().all()

        for transaction in user_recurring_transactions:
            already_processed = await self.check_recurring_transaction_history(transaction.id, transaction.next_due_date)

            if not already_processed:
                try:
                    await self.transaction_repo.add_user_transaction(
                        transaction_name=transaction.name,
                        transaction_amount=transaction.amount,
                        currency_code=transaction.currency_id,
                        user_id=transaction.user_id,
                        category_id=transaction.category_id,
                    )

                    recurring_history_transaction = RecurringTransactionHistory(recurring_transaction_id=transaction.id)
                    self.db.add(recurring_history_transaction)

                    next_due = self._calculate_next_due_date_from_date(transaction.next_due_date, transaction.frequency)
                    recurring_transaction = await self.db.get(RecurringTransaction, transaction.id)
                    recurring_transaction.next_due_date = next_due
                        
                    await self.db.commit()
                    
                except Exception as e:
                    raise ValueError(f"Failed to process recurring transaction {transaction.id}: {str(e)}") from e
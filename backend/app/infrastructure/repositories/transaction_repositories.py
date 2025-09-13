from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID, uuid4
from asyncpg import Connection

from app.infrastructure.repositories.user_repositories import UserRepository
from app.schemas.transaction_schema import CategoryType, RecurringFrequency

class TransactionRepository:
    def __init__(self, conn: Connection):
        self.conn = conn
        self.user_repo = UserRepository(conn)
    
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

    async def get_all_user_transactions(
        self, 
        user_id: UUID, 
        category_type: CategoryType | None, 
        created_at: tuple[datetime, datetime] | None
    ):
        query = """
            SELECT t.* 
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = $1
        """
        params = [user_id]
        
        if category_type:
            query += " AND c.type = $" + str(len(params) + 1)
            params.append(category_type)

        if created_at:
            start_date, end_date = created_at
            query += " AND t.created_at >= $" + str(len(params) + 1)
            query += " AND t.created_at <= $" + str(len(params) + 2)
            params.extend([start_date, end_date])

            
        rows = await self.conn.fetch(query, *params)
        return [dict(row) for row in rows]
    
    async def check_category_exists(self, category_id: UUID) -> bool:
        row = await self.conn.fetchval("""
            SELECT EXISTS(SELECT 1 FROM categories WHERE id = $1)
        """, category_id)
        return row
    
    async def get_category_type(self, category_id: UUID) -> str:
        category = await self.conn.fetchrow(
            "SELECT type FROM categories WHERE id = $1",
            category_id
        )
        if not category:
            raise ValueError("Category not found")
        
        return category["type"]


    async def add_user_transaction(
        self, 
        transaction_id: UUID, 
        transaction_name: str, 
        transaction_amount: Decimal, 
        currency_code: str,
        user_id: UUID,
        category_id: UUID
    ):  
        category_type = self.get_category_type(category_id)
        
        try:
            async with self.conn.transaction():
                tx_row = await self.conn.fetchrow("""
                    INSERT INTO transactions(id, name, amount, currency_id, user_id, category_id)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id, name, amount, currency_id, user_id, category_id
                """, transaction_id, transaction_name, transaction_amount, currency_code, user_id, category_id)
                
                if not tx_row:
                    raise ValueError("Failed to insert transaction")
                
                user_update = self.user_repo.update_user_balance(category_type, transaction_amount, user_id)
                if not user_update:
                    raise ValueError(f"Failed to update balance for user {user_id}")
                
                return dict(tx_row)
        except Exception as e:
            raise ValueError(f"Failed to process transaction: {str(e)}") from e
        
    async def add_user_recurring_transaction(
        self, 
        transaction_id: UUID, 
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
                actual_due_date = self._calculate_next_due_date_from_now(frequency)
            else:
                actual_due_date = next_due_date

            async with self.conn.transaction():
                tx_row = await self.conn.fetchrow("""
                    INSERT INTO recurring_transactions(
                        id, name, amount, currency_id, user_id, 
                        category_id, frequency, next_due_date
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    RETURNING *
                """, transaction_id, transaction_name, transaction_amount, 
                    currency_code, user_id, category_id, frequency, actual_due_date)
                
                if not tx_row:
                    raise ValueError("Failed to insert recurring transaction")
                
                if create_immediate_transaction:
                    actual_transaction_id = uuid4()
                    actual_tx_row = await self.conn.fetchrow("""
                        INSERT INTO transactions(id, name, amount, currency_id, user_id, category_id)
                        VALUES ($1, $2, $3, $4, $5, $6)
                        RETURNING *
                    """, actual_transaction_id, transaction_name, transaction_amount, 
                        currency_code, user_id, category_id)
                    
                    if not actual_tx_row:
                        raise ValueError("Failed to insert actual transaction")
                    
                    category_type = await self.get_category_type(category_id)
                    user_update = await self.user_repo.update_user_balance(category_type, transaction_amount, user_id)
                    if not user_update:
                        raise ValueError(f"Failed to update balance for user {user_id}")
                    
                    history_id = uuid4()
                    await self.conn.execute("""
                        INSERT INTO recurring_transaction_history (id, recurring_transaction_id)
                        VALUES ($1, $2)
                    """, history_id, tx_row["id"])
                
                return dict(tx_row)
        except Exception as e:
            raise ValueError(f"Failed to process recurring transaction: {str(e)}") from e
        

    async def check_recurring_transaction_history(self, recurring_transaction_id: UUID, target_date: datetime):
        """Check if a recurring transaction has already been triggered for a specific date."""
        return await self.conn.fetchval("""
            SELECT EXISTS(
                SELECT 1 FROM recurring_transaction_history
                WHERE recurring_transaction_id = $1 
                AND DATE(triggered_at) = DATE($2)
            )
        """, recurring_transaction_id, target_date)

    async def check_recurring_transaction(self, user_id: UUID):
        """Check and process all due recurring transactions for a user."""
        transactions_rows = await self.conn.fetch("""
            SELECT id, name, amount, currency_id, category_id, frequency, next_due_date 
            FROM recurring_transactions
            WHERE user_id = $1 
            AND next_due_date <= $2
        """, user_id, datetime.now(timezone.utc))
        
        user_recurring_transactions = [dict(row) for row in transactions_rows]

        for transaction in user_recurring_transactions:
            already_processed = await self.check_recurring_transaction_history(
                transaction["id"], 
                transaction["next_due_date"]
            )
            
            if not already_processed:
                try:
                    async with self.conn.transaction():
                        actual_transaction_id = uuid4()
                        await self.conn.execute("""
                            INSERT INTO transactions(id, name, amount, currency_id, user_id, category_id)
                            VALUES ($1, $2, $3, $4, $5, $6)
                        """, actual_transaction_id, transaction["name"], transaction["amount"], 
                            transaction["currency_id"], user_id, transaction["category_id"])
                        
                        category_type = await self.get_category_type(transaction["category_id"])
                        user_update = await self.user_repo.update_user_balance(
                            category_type, transaction["amount"], user_id
                        )
                        if not user_update:
                            raise ValueError(f"Failed to update balance for user {user_id}")
                        
                        history_id = uuid4()
                        await self.conn.execute("""
                            INSERT INTO recurring_transaction_history (id, recurring_transaction_id)
                            VALUES ($1, $2)
                        """, history_id, transaction["id"])
                        
                        next_due = self._calculate_next_due_date_from_date(
                            transaction["next_due_date"], 
                            transaction["frequency"]
                        )
                        await self.conn.execute("""
                            UPDATE recurring_transactions 
                            SET next_due_date = $1 
                            WHERE id = $2
                        """, next_due, transaction["id"])
                        
                except Exception as e:
                    raise ValueError(f"Failed to process recurring transaction {transaction['id']}: {str(e)}") from e


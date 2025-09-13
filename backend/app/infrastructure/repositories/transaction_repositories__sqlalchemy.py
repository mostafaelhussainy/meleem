from decimal import Decimal
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import exists
from datetime import datetime

from ...models.transaction import Transaction
from ...models.category import Category
from ...schemas.transaction_schema import CategoryType, RecurringFrequency
from ...infrastructure.repositories.user_repositories__sqlalchemy import SQLAlchemyUserRepository

class SQLAlchemyTransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = SQLAlchemyUserRepository(db)
    
    async def get_all_user_transactions(
        self,
        user_id: UUID,
        category_type: CategoryType | None,
        created_at: tuple[datetime, datetime] | None,
    ) -> list[Transaction]:
        query = (
            select(Transaction)
            .join(Category, Transaction.category_id == Category.id)
            .where(Transaction.user_id == user_id)
        )

        if category_type:
            query = query.where(Category.type == category_type)

        if created_at:
            start_date, end_date = created_at
            query = query.where(
                Transaction.created_at >= start_date,
                Transaction.created_at <= end_date,
            )

        result = await self.db.execute(query)
        return result.scalars().all()


    async def check_category_exists(self, category_id: UUID) -> bool:
        stmt = select(exists().where(Category.id == category_id))
        result = await self.db.execute(stmt)
        return result.scalar()

    async def get_category_type(self, category_id: UUID) -> str:
        category_type_orm = await self.db.execute(select(Category.type).where(Category.id == category_id))
        category_type = category_type_orm.scalar()
        if category_type is None:
            raise ValueError("Category not found")
        return category_type

    async def add_user_transaction(
        self, 
        transaction_name: str, 
        transaction_amount: Decimal, 
        currency_code: str,
        user_id: UUID,
        category_id: UUID
    ):  
        category_type = await self.get_category_type(category_id)
        
        try:
            transaction = Transaction(
                name=transaction_name, 
                amount=transaction_amount, 
                currency_id=currency_code, 
                user_id=user_id, 
                category_id=category_id
            )
            self.db.add(transaction)
            await self.user_repo.update_user_balance(category_type, transaction_amount, user_id)
            await self.db.commit()
            await self.db.refresh(transaction)

            return transaction.__dict__
        except Exception as e:
            await self.db.rollback()
            raise ValueError(f"Failed to process transaction: {str(e)}") from e

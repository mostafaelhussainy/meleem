from typing import Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from ...models.user import User

class SQLAlchemyUserRepository:
    def __init__(
        self,
        db: AsyncSession
    ):
        self.db = db

    async def get_user_details(self, user_id: UUID):
        return await self.db.get(User, user_id)

    async def update_user(
        self,
        id: UUID,
        name: Optional[str] = None,
        email: Optional[str] = None,
        currency_code: Optional[str] = None,
        goal: Optional[Decimal] = None,
        savings: Optional[Decimal] = None,
        balance: Optional[Decimal] = None,
    ) -> Optional[User]:
        user = await self.db.get(User, id)
        if not user:
            return None

        if email is not None:
            user.email = email
        if name is not None:
            user.name = name
        if currency_code is not None:
            user.currency_code = currency_code
        if goal is not None:
            user.goal = goal
        if savings is not None:
            user.savings = savings
        if balance is not None:
            user.balance = balance

        await self.db.commit()
        await self.db.refresh(user)  

        return user

    async def update_user_balance(
        self,
        category_type: str,
        transaction_amount: Decimal,
        user_id: UUID,
    ) -> User:
        user = await self.db.get(User, user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")

        balance_change = transaction_amount if category_type == "income" else -transaction_amount
        user.balance = (user.balance or 0) + balance_change

        await self.db.commit()
        await self.db.refresh(user)

        return user
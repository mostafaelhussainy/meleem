
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from decimal import Decimal

from app.models.user import User


class SQLAlchemyAuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        return user.__dict__ if user else None
        
    async def create_user(self, id: UUID, name: str, email: str, hashed_password: str, 
                         currency_code: str, goal: Decimal, savings: Decimal, balance: Decimal):
        user = User(
            id=id,
            name=name,
            email=email,
            hashed_password=hashed_password,
            currency_code=currency_code,
            goal=goal,
            savings=savings,
            balance=balance
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user.id 
        
    async def get_user_by_id(self, user_id: UUID):
        result = await self.db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        return user.__dict__ if user else None
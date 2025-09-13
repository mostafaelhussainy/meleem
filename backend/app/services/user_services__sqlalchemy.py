from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from ..infrastructure.repositories.user_repositories__sqlalchemy import SQLAlchemyUserRepository
from ..schemas.user_schema import UpdateUserRequest
from ..core.exceptions.exceptions import UserDoesNotExistException

class SQLAlchemyUserService:
    def __init__(
        self,
        db: AsyncSession
    ):
        self.repo = SQLAlchemyUserRepository(db)

    async def get_user_details(self, user_id: UUID):
        user = await self.repo.get_user_details(user_id)
        return user

    async def update_user(
        self, 
        user_id: UUID, 
        request: UpdateUserRequest
    ):
        user = await self.repo.update_user(
            user_id,
            name=request.name,
            email=request.email,
            currency_code=request.currency_code,
            goal=request.goal,
            savings=request.savings,
            balance=request.balance
        )
        if not user:
            raise UserDoesNotExistException("User doesn't exist")
        return user

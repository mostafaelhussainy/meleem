from uuid import UUID
from asyncpg import Connection


from ..schemas.user_schema import UpdateUserRequest
from ..core.exceptions.exceptions import UserDoesNotExistException
from ..infrastructure.repositories.auth_repositories import AuthRepository
from ..infrastructure.repositories.user_repositories import UserRepository

class UserService:
    def __init__(self, conn: Connection):
        self.repo = UserRepository(conn)
        self.auth_repo = AuthRepository(conn)

    async def update_user(self, user_id: UUID, request: UpdateUserRequest):
        existing = await self.auth_repo.get_user_by_id(user_id)
        if not existing:
            raise UserDoesNotExistException("User doesn't exist")
        
        return await self.repo.update_user(
            user_id,
            name=request.name if request.name is not None else existing['name'],
            email=request.email if request.email is not None else existing['email'],
            currency_code=request.currency_code if request.currency_code is not None else existing['currency_code'],
            goal=request.goal if request.goal is not None else existing['goal'],
            savings=request.savings if request.savings is not None else existing['savings'],
            balance=request.balance if request.balance is not None else existing['balance']
        )
    
    async def get_user_details(self, user_id: UUID):
        return await self.repo.get_user_details(user_id)

         
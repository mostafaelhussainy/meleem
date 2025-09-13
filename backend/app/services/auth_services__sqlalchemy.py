import uuid
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from app.core.config import settings
from app.core.security import AuthSecurity
from app.schemas.auth_schema import LoginUserRequest, RegisterUserRequest
from app.infrastructure.repositories.auth_repository__sqlalchemy import SQLAlchemyAuthRepository
from app.infrastructure.repositories.recurring_transaction_repository__sqlalchemy import SQLAlchemyRecurringTransactionRepository
from app.core.exceptions.exceptions import InvalidPasswordException, UserAlreadyExistException, UserEmailDoesNotExistException


class SQLAlchemyAuthService:
    def __init__(self, db: AsyncSession):
        self.repo = SQLAlchemyAuthRepository(db)
        self.security = AuthSecurity()
        self.recurring_repo = SQLAlchemyRecurringTransactionRepository(db)

    def create_token(self, user_id: uuid.UUID) -> str:
        payload = {
            'sub': str(user_id),
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    async def register_user(self, request: RegisterUserRequest) -> uuid.UUID:
        existing = await self.repo.get_user_by_email(request.email)
        if existing:
            raise UserAlreadyExistException("User with the same email already exists")
        
        user_uuid = uuid.uuid4()
        hashed_password = self.security.hash_password(request.password)
        return await self.repo.create_user(
            user_uuid, 
            request.name, 
            request.email, 
            hashed_password, 
            request.currency_code, 
            request.goal, 
            request.savings, 
            request.balance
        )

    async def login_user(self, request: LoginUserRequest):
        user = await self.repo.get_user_by_email(request.email)
        if not user:
            raise UserEmailDoesNotExistException("Email does not exist")

        valid_password = self.security.verify_password(request.password, user["hashed_password"])
        if not valid_password:
            raise InvalidPasswordException("Password is incorrect")
        
        user_id = user["id"]
        
        # Skip recurring transaction check for now
        await self.recurring_repo.check_recurring_transaction(user_id)

        return user_id
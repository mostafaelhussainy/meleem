import uuid
from asyncpg import Connection
from datetime import datetime, timedelta

import jwt

from ..core.config import settings
from ..core.security import AuthSecurity
from ..schemas.auth_schema import LoginUserRequest, RegisterUserRequest
from ..infrastructure.repositories.auth_repositories import AuthRepository
from ..infrastructure.repositories.transaction_repositories import TransactionRepository
from ..core.exceptions.exceptions import InvalidPasswordException, UserAlreadyExistException, UserEmailDoesNotExistException


class AuthService:
    def __init__(self, conn: Connection):
        self.repo = AuthRepository(conn)
        self.security = AuthSecurity()
        self.transaction_repo = TransactionRepository(conn)

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
        return await self.repo.create_user(user_uuid, request.name, request.email, hashed_password, request.currency_code, request.goal, request.savings, request.balance)

    async def login_user(self, request: LoginUserRequest):
        user = await self.repo.get_user_by_email(request.email)
        if not user:
            raise UserEmailDoesNotExistException("Email does not exist")

        valid_password = self.security.verify_password(request.password, user["hashed_password"])
        if not valid_password:
            raise InvalidPasswordException("Password is incorrect")
        
        user_id = user["id"]

        await self.transaction_repo.check_recurring_transaction(user_id)

        return user_id


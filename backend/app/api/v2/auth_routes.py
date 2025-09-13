from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...services.auth_services__sqlalchemy import SQLAlchemyAuthService
from ...infrastructure.db.database import get_db
from ...schemas.auth_schema import LoginUserRequest, RegisterUserRequest, TokenResponse

router = APIRouter()

@router.post('/register', response_model=TokenResponse)
async def register_user(
    request: RegisterUserRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = SQLAlchemyAuthService(db)
    user_id = await auth_service.register_user(request)
    token = auth_service.create_token(user_id)
    return {'token': token, 'token_type': 'Bearer'}

@router.post('/login', response_model=TokenResponse)
async def login_user(
    request: LoginUserRequest,
    db: AsyncSession = Depends(get_db)
):
    auth_service = SQLAlchemyAuthService(db)
    user_id = await auth_service.login_user(request)
    token = auth_service.create_token(user_id)
    return {'token': token, 'token_type': 'Bearer'}
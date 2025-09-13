from asyncpg import Connection
from fastapi import APIRouter, Depends

from ...services.auth_services import AuthService
from ...infrastructure.db.connection import get_db_connection
from ...schemas.auth_schema import LoginUserRequest, RegisterUserRequest, TokenResponse

router = APIRouter()

@router.post('/register', response_model=TokenResponse)
async def register_user(
    request: RegisterUserRequest,
    conn: Connection = Depends(get_db_connection)
):
    auth_service = AuthService(conn)
    user_id = await auth_service.register_user(request)
    token = auth_service.create_token(user_id)
    return {'token': token, 'token_type': 'Bearer'}

@router.post('/login', response_model=TokenResponse)
async def login_user(
    request: LoginUserRequest,
    conn: Connection = Depends(get_db_connection)
):
    auth_service = AuthService(conn)
    user_id = await auth_service.login_user(request)
    token = auth_service.create_token(user_id)
    return {'token': token, 'token_type': 'Bearer'}

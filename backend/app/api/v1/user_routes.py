from asyncpg import Connection
from fastapi import APIRouter, Depends
from uuid import UUID

from ...services.user_services import UserService
from ...core.dependencies.auth import get_current_user
from ...infrastructure.db.connection import get_db_connection
from ...schemas.user_schema import UpdateUserRequest, UpdateUserResponse, UserDetailsResponse


router = APIRouter()


@router.get('/', response_model=UserDetailsResponse)
async def get_user_details(
    user_id: UUID = Depends(get_current_user),
    conn: Connection = Depends(get_db_connection),
):
    user_service = UserService(conn)
    return await user_service.get_user_details(user_id)

@router.post('/update-user', response_model=UpdateUserResponse)
async def update_user(
    request: UpdateUserRequest,
    user_id: UUID = Depends(get_current_user),
    conn: Connection = Depends(get_db_connection),
):
    user_service = UserService(conn)
    return await user_service.update_user(user_id, request)




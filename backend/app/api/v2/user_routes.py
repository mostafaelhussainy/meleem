from fastapi import APIRouter, Depends
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ...infrastructure.db.database import get_db
from ...core.dependencies.auth import get_current_user
from ...services.user_services__sqlalchemy import SQLAlchemyUserService
from ...schemas.user_schema import UpdateUserRequest, UpdateUserResponse, UserDetailsResponse


router = APIRouter()


@router.get('/', response_model=UserDetailsResponse)
async def get_user_details(
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_service = SQLAlchemyUserService(db)
    return await user_service.get_user_details(user_id)

@router.post('/update-user', response_model=UpdateUserResponse)
async def update_user(
    request: UpdateUserRequest,
    user_id: UUID = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_service = SQLAlchemyUserService(db)
    return await user_service.update_user(user_id, request)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...infrastructure.db.database import get_db
from ...services.listing_services__sqlalchemy import SQLAlchemyListingService

router = APIRouter()

@router.get('/currencies')
async def get_currencies_list(db: AsyncSession = Depends(get_db)):
    listing_service = SQLAlchemyListingService(db)
    return await listing_service.get_currencies_list()

@router.get('/categories')
async def get_categories_list(db: AsyncSession = Depends(get_db)):
    listing_service = SQLAlchemyListingService(db)
    return await listing_service.get_categories_list()
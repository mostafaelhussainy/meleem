from asyncpg import Connection
from fastapi import APIRouter, Depends

from app.infrastructure.db.connection import get_db_connection
from app.services.listing_services import ListingService

router = APIRouter()

@router.get('/currencies')
async def get_currencies_list(conn: Connection = Depends(get_db_connection)):
    listing_service = ListingService(conn)
    return await listing_service.get_currencies_list()

@router.get('/categories')
async def get_categories_list(conn: Connection = Depends(get_db_connection)):
    listing_service = ListingService(conn)
    return await listing_service.get_categories_list()
from app.core.cache import cache_response
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.repositories.listing_repository__sqlalchemy import SQLAlchemyListingRepository


class SQLAlchemyListingService:
    def __init__(self, db: AsyncSession):
        self.repo = SQLAlchemyListingRepository(db)

    @cache_response(prefix="currencies_list", expire=300)
    async def get_currencies_list(self):
        currencies_list = await self.repo.get_currencies_list()
        return currencies_list
    
    @cache_response(prefix="categories_list", expire=300)
    async def get_categories_list(self):
        categories_list = await self.repo.get_categories_list()
        return categories_list

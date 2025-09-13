from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.currency import Currency
from app.models.category import Category

class SQLAlchemyListingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_currencies_list(self):
        result = await self.db.execute(select(Currency))
        currencies = result.scalars().all()
        return [currency.__dict__ for currency in currencies]
    
    async def get_categories_list(self):
        result = await self.db.execute(select(Category))
        categories = result.scalars().all()
        return [category.__dict__ for category in categories]
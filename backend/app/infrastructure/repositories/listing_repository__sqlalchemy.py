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
        return [{
            'code': currency.iso_code,
            'name': currency.name,
            'symbol': currency.symbol
        } for currency in currencies]
    
    async def get_categories_list(self):
        result = await self.db.execute(select(Category))
        categories = result.scalars().all()
        return [{
            'id': str(category.id),
            'name': category.name,
            'type': category.type.value  
        } for category in categories]
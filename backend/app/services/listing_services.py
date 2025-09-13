from asyncpg import Connection

from app.infrastructure.repositories.listing_repositories import ListingRepository


class ListingService:
    def __init__(self, conn: Connection):
        self.repo = ListingRepository(conn)

    async def get_currencies_list(self):
        currencies_list = await self.repo.get_currencies_list()
        return currencies_list
    
    async def get_categories_list(self):
        categories_list = await self.repo.get_categories_list()
        return categories_list

from asyncpg import Connection


class ListingRepository:
    def __init__(self, conn: Connection):
        self.conn = conn

    async def get_currencies_list(self):
        rows = await self.conn.fetch("""
            SELECT * FROM currencies;
        """)
        return [dict(row) for row in rows] 
    
    async def get_categories_list(self):
        rows = await self.conn.fetch("""
            SELECT * FROM categories
        """)
        return [dict(row) for row in rows] 


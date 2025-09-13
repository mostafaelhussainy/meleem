import asyncpg
from app.core.config import settings

pool: asyncpg.pool.Pool | None = None

async def connect_to_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME,
            min_size=settings.DB_MIN_CONNECTIONS,
            max_size=settings.DB_MAX_CONNECTIONS,
        )
    return pool

async def disconnect_from_db():
    global pool
    if pool:
        await pool.close()
        pool = None

async def get_db_connection():
    if pool is None:
        raise Exception("Pool is not initialized. Did you call connect_to_db()?")

    async with pool.acquire() as conn:
        yield conn

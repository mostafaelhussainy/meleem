from typing import Optional
from redis import asyncio as aioredis
from app.core.config import settings

class RedisManager:
    _redis: Optional[aioredis.Redis] = None

    @classmethod
    async def get_redis(cls) -> aioredis.Redis:
        if cls._redis is None:
            cls._redis = await aioredis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                encoding="utf-8",
                decode_responses=True
            )
        return cls._redis

    @classmethod
    async def close(cls):
        if cls._redis is not None:
            await cls._redis.close()
            cls._redis = None

redis_manager = RedisManager()

async def get_redis_connection() -> aioredis.Redis:
    return await redis_manager.get_redis()

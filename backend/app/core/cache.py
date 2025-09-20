import time
import json
from functools import wraps
from typing import Callable
from app.infrastructure.db.redis_connection import get_redis_connection
 
def cache_response(prefix: str, expire: int = 3600):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if args and hasattr(args[0], '__class__'):  
                cache_key = f"{prefix}:{args[0].__class__.__name__}:{func.__name__}"
            else:
                cache_key = f"{prefix}:{func.__name__}"
            
            if kwargs:
                cache_key += f":{json.dumps(sorted(kwargs.items()))}"
            
            redis = await get_redis_connection()
            start_time = time.perf_counter()

            cached_response = await redis.get(cache_key)
            if cached_response:
                duration = (time.perf_counter() - start_time) * 1000
                print(f"[CACHE HIT] {cache_key} took {duration:.2f} ms")
                return json.loads(cached_response)

            response = await func(*args, **kwargs)

            duration = (time.perf_counter() - start_time) * 1000
            print(f"[CACHE MISS] {cache_key} took {duration:.2f} ms") 

            await redis.setex(cache_key, expire, json.dumps(response))
            return response
        return wrapper
    return decorator

from fastapi import Depends, Request
from redis.asyncio.client import Redis
from src.application.contracts import ICache
from src.infrastructure.cache import KeydbCache


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


def get_cache(redis_client: Redis = Depends(get_redis)) -> ICache:
    return KeydbCache(redis_client)

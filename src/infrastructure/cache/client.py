import redis.asyncio as redis
from redis.asyncio.client import Redis
from src.infrastructure.config import settings


def create_redis_client() -> Redis:
    kw = {
        'max_connections': 50,
        'decode_responses': True,
        'socket_timeout': 5,
        'socket_connect_timeout': 5,
        'health_check_interval': 30,
        'retry_on_timeout': True,
        'socket_keepalive': True,
    }
    if settings.REDIS_PASSWORD:
        kw['password'] = settings.REDIS_PASSWORD
    return redis.from_url(settings.REDIS_URL, **kw)
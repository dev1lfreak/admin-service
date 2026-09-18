from redis.asyncio.client import Redis
from src.application.contracts import ICache


class KeydbCache(ICache):
    def __init__(self, redis_client: Redis):
        self._r = redis_client

    async def set(self, key: str, value: str, ttl: int) -> None:
        return bool(await self._r.set(key, value, ex=ttl))

    async def set_nx(self, key: str, value: str, ttl: int) -> bool:
        return bool(await self._r.set(key, value, ex=ttl, nx=True))

    async def get(self, key: str) -> str | None:
        return await self._r.get(key)

    async def delete(self, key: str) -> bool:
        deleted = await self._r.delete(key)
        return deleted > 0

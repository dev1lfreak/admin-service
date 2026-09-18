from abc import ABC, abstractmethod


class ICache(ABC):

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def set_nx(self, key: str, value: str, ttl: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def get(self, key: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> bool:
        raise NotImplementedError
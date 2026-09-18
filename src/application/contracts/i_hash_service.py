from abc import ABC, abstractmethod


class IHashService(ABC):

    @abstractmethod
    async def hash(self, value: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def verify(self, hashed_value: str, plain_value: str) -> bool:
        raise NotImplementedError
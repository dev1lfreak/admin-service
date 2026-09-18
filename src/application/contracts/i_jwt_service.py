from abc import ABC, abstractmethod

from src.application.domain.dto import AccessTokenPayload, RefreshTokenPayload


class IJwtService(ABC):
    @abstractmethod
    async def create_access_token(self, user_id: str, *, role: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def create_refresh_token(self, user_id: str, *, role: str) -> str:
        raise NotImplementedError

    @abstractmethod
    async def decode_access_token(self, token: str) -> AccessTokenPayload:
        raise NotImplementedError

    @abstractmethod
    async def decode_refresh_token(self, token: str) -> RefreshTokenPayload:
        raise NotImplementedError

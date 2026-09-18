from abc import ABC, abstractmethod
from datetime import datetime

from src.application.domain.entities import UserEntity
from src.application.domain.entities.party_search import PartySearchEntity


class IUserRepository(ABC):
    @abstractmethod
    async def create_legal_entity_user(
        self,
        *,
        email: str,
        password_hash: str,
        provisioned_by: str,
        provisioned_at: datetime,
        kyc_verified: bool,
        kyc_verified_at: datetime,
    ) -> UserEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def list_all(self, *, limit: int, offset: int, search: str | None = None) -> list[UserEntity]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def search_individuals(self, *, query: str, limit: int, offset: int) -> list[PartySearchEntity]:
        raise NotImplementedError

    @abstractmethod
    async def count_individuals(self, *, query: str) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_all(self, *, search: str) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def set_password(self, user_id: str, password_hash: str) -> UserEntity:
        raise NotImplementedError

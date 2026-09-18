from abc import ABC, abstractmethod
from typing import Any

from src.application.domain.entities.organization import PurchaseRequestEntity


class IPurchaseRequestRepository(ABC):
    @abstractmethod
    async def create(self, values: dict[str, Any]) -> PurchaseRequestEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, request_id: str) -> PurchaseRequestEntity:
        raise NotImplementedError

    @abstractmethod
    async def list_all(
        self,
        *,
        status: str | None,
        organization_id: str | None,
        limit: int,
        offset: int,
    ) -> list[PurchaseRequestEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, request_id: str, *, values: dict[str, Any]) -> PurchaseRequestEntity:
        raise NotImplementedError

    @abstractmethod
    async def count_all(self, *, status: str | None, organization_id: str | None) -> int:
        raise NotImplementedError

    @abstractmethod
    async def count_for_month(
        self, 
        *,
        year: int, 
        month: int, 
        status: str | None, 
        organization_id: str | None
    ) -> int:
        raise NotImplementedError
    
    @abstractmethod
    async def count_for_day(
        self, 
        *, 
        year: int, 
        month: int, 
        day: int, 
        status: str | None, 
        organization_id: str | None
    ) -> int:
        raise NotImplementedError
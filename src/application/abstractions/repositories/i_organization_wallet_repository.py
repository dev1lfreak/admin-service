from abc import ABC, abstractmethod

from src.application.domain.entities.organization import OrganizationWalletEntity


class IOrganizationWalletRepository(ABC):
    @abstractmethod
    async def create_many(self, wallets: list[OrganizationWalletEntity]) -> list[OrganizationWalletEntity]:
        raise NotImplementedError

    @abstractmethod
    async def list_by_organization(self, organization_id: str) -> list[OrganizationWalletEntity]:
        raise NotImplementedError

    @abstractmethod
    async def exists_for_organization(self, organization_id: str) -> bool:
        raise NotImplementedError

from abc import ABC, abstractmethod

from src.application.domain.entities.user import WalletEntity


class IWalletRepository(ABC):

    @abstractmethod
    async def list_by_user(self, user_id: str) -> list[WalletEntity]:
        raise NotImplementedError

    @abstractmethod
    async def exists_for_user(self, user_id: str) -> bool:
        raise NotImplementedError
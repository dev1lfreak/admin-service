from abc import ABC, abstractmethod

from src.application.domain.entities.admin_user import AdminUserEntity


class IAdminUserRepository(ABC):
    @abstractmethod
    async def get_by_login(self, login: str) -> AdminUserEntity:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, admin_user_id: str) -> AdminUserEntity:
        raise NotImplementedError

    @abstractmethod
    async def update_last_login(self, admin_user_id: str, *, last_login_at) -> None:
        raise NotImplementedError

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from src.application.domain.entities.admin_session import AdminSessionEntity


class IAdminSessionRepository(ABC):
    @abstractmethod
    async def get_by_sid(self, sid: str) -> Optional[AdminSessionEntity]:
        raise NotImplementedError

    @abstractmethod
    async def upsert_by_device(
        self,
        *,
        admin_user_id: str,
        device_id: str,
        sid: str,
        refresh_jti_hash: str,
        refresh_expires_at: datetime,
        user_agent: str | None,
        ip: str | None,
        now: datetime,
    ) -> AdminSessionEntity:
        raise NotImplementedError

    @abstractmethod
    async def revoke_by_sid(self, sid: str, now: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rotate_refresh_if_match(
        self,
        *,
        sid: str,
        old_jti_hash: str,
        new_jti_hash: str,
        new_refresh_expires_at: datetime,
        now: datetime,
        ip: str | None,
        user_agent: str | None,
    ) -> bool:
        raise NotImplementedError

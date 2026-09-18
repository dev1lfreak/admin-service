from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.abstractions.repositories import IAdminSessionRepository
from src.application.contracts import ILogger
from src.application.domain.entities.admin_session import AdminSessionEntity
from src.infrastructure.database.models import AdminSessionModel


class AdminSessionRepository(IAdminSessionRepository):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self._session = session
        self._logger = logger

    def _to_entity(self, m: AdminSessionModel) -> AdminSessionEntity:
        return AdminSessionEntity(
            sid=m.sid,
            admin_user_id=m.admin_user_id,
            device_id=m.device_id,
            revoked_at=m.revoked_at,
            last_seen_at=m.last_seen_at,
            refresh_jti_hash=m.refresh_jti_hash,
            refresh_expires_at=m.refresh_expires_at,
            user_agent=m.user_agent,
            first_ip=m.first_ip,
            last_ip=m.last_ip,
        )

    async def get_by_sid(self, sid: str) -> Optional[AdminSessionEntity]:
        res = await self._session.execute(select(AdminSessionModel).where(AdminSessionModel.sid == sid))
        m = res.scalar_one_or_none()
        return self._to_entity(m) if m else None

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
        res = await self._session.execute(
            select(AdminSessionModel).where(
                AdminSessionModel.admin_user_id == admin_user_id,
                AdminSessionModel.device_id == device_id,
            )
        )
        m = res.scalar_one_or_none()
        if m is None:
            m = AdminSessionModel(
                sid=sid,
                admin_user_id=admin_user_id,
                device_id=device_id,
                revoked_at=None,
                last_seen_at=now,
                refresh_jti_hash=refresh_jti_hash,
                refresh_expires_at=refresh_expires_at,
                user_agent=user_agent,
                first_ip=ip,
                last_ip=ip,
            )
            self._session.add(m)
        else:
            m.sid = sid
            m.revoked_at = None
            m.last_seen_at = now
            m.refresh_jti_hash = refresh_jti_hash
            m.refresh_expires_at = refresh_expires_at
            m.user_agent = user_agent
            m.last_ip = ip
        await self._session.flush()
        return self._to_entity(m)

    async def revoke_by_sid(self, sid: str, now: datetime) -> None:
        await self._session.execute(
            update(AdminSessionModel)
            .where(AdminSessionModel.sid == sid, AdminSessionModel.revoked_at.is_(None))
            .values(revoked_at=now)
        )
        await self._session.flush()

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
        values = {
            'refresh_jti_hash': new_jti_hash,
            'refresh_expires_at': new_refresh_expires_at,
            'last_seen_at': now,
            'user_agent': user_agent,
        }
        if ip is not None:
            values['last_ip'] = ip
        res = await self._session.execute(
            update(AdminSessionModel)
            .where(
                AdminSessionModel.sid == sid,
                AdminSessionModel.revoked_at.is_(None),
                AdminSessionModel.refresh_jti_hash == old_jti_hash,
            )
            .values(**values)
        )
        await self._session.flush()
        return (res.rowcount or 0) > 0

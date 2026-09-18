from __future__ import annotations

from datetime import datetime

from fastapi import status
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.application.abstractions.repositories import IAdminUserRepository
from src.application.contracts import ILogger
from src.application.domain.entities.admin_user import AdminUserEntity
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.database.models import AdminUserModel


class AdminUserRepository(IAdminUserRepository):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self._session = session
        self._logger = logger

    def _to_entity(self, m: AdminUserModel) -> AdminUserEntity:
        return AdminUserEntity(
            id=m.id,
            login=m.login,
            password_hash=m.password_hash,
            first_name=m.first_name,
            last_name=m.last_name,
            role=m.role,
            is_active=m.is_active,
            last_login_at=m.last_login_at,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    async def get_by_login(self, login: str) -> AdminUserEntity:
        try:
            stmt = select(AdminUserModel).where(func.lower(AdminUserModel.login) == login.lower())
            result = await self._session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise ApplicationException(status_code=status.HTTP_404_NOT_FOUND, message='Admin user not found')
            return self._to_entity(user)
        except ApplicationException:
            raise
        except SQLAlchemyError as exc:
            self._logger.exception(str(exc))
            raise ApplicationException(status_code=500, message='Database error')

    async def get_by_id(self, admin_user_id: str) -> AdminUserEntity:
        try:
            stmt = select(AdminUserModel).where(AdminUserModel.id == admin_user_id)
            result = await self._session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                raise ApplicationException(status_code=status.HTTP_404_NOT_FOUND, message='Admin user not found')
            return self._to_entity(user)
        except ApplicationException:
            raise
        except SQLAlchemyError as exc:
            self._logger.exception(str(exc))
            raise ApplicationException(status_code=500, message='Database error')

    async def update_last_login(self, admin_user_id: str, *, last_login_at: datetime) -> None:
        await self._session.execute(
            update(AdminUserModel)
            .where(AdminUserModel.id == admin_user_id)
            .values(last_login_at=last_login_at)
        )
        await self._session.flush()

from __future__ import annotations

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.admin_user import AdminUserEntity
from src.infrastructure.database.decorators import transactional


class GetAdminMeCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, admin_user_id: str) -> AdminUserEntity:
        return await self._unit_of_work.admin_user_repository.get_by_id(admin_user_id)

from __future__ import annotations

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.user import UserEntity
from src.infrastructure.database.decorators import transactional


class ListUsersCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(
        self,
        *,
        limit: int = 50,
        offset: int = 0,
        search: str | None = None,
    ) -> tuple[list[UserEntity], int]:
        items = await self._unit_of_work.user_repository.list_all(
            limit=limit,
            offset=offset,
            search=search,
        )
        total = await self._unit_of_work.user_repository.count_all(search=search)
        return items, total


class GetUserCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, user_id: str) -> UserEntity:
        return await self._unit_of_work.user_repository.get_by_id(user_id)

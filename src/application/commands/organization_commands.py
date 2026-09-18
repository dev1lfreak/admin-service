from __future__ import annotations

from typing import Any

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.organization import LegalEntityEntity
from src.infrastructure.database.decorators import transactional


class ListOrganizationsCommand:
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
    ) -> tuple[list[LegalEntityEntity], int]:
        items = await self._unit_of_work.legal_entity_repository.list_all(
            limit=limit,
            offset=offset,
            search=search,
        )
        total = await self._unit_of_work.legal_entity_repository.count_all(search=search)
        return items, total


class GetOrganizationCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, organization_id: str) -> LegalEntityEntity:
        return await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)


class UpdateOrganizationCommand:
    ALLOWED_FIELDS = frozenset({
        'name', 'short_name', 'ogrn', 'kpp', 'legal_address', 'actual_address',
        'bank_details', 'contact_person', 'contact_phone', 'status',
    })

    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, organization_id: str, *, values: dict[str, Any]) -> LegalEntityEntity:
        filtered = {k: v for k, v in values.items() if k in self.ALLOWED_FIELDS and v is not None}
        return await self._unit_of_work.legal_entity_repository.update(organization_id, values=filtered)

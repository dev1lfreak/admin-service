from __future__ import annotations

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.organization import LegalEntityEntity 
from src.application.domain.entities.party_search import PartySearchEntity
from src.application.domain.enums.account_type import AccountType
from src.infrastructure.database.decorators import transactional


class SearchPartiesCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, *, query: str, limit: int = 50, offset: int = 0) -> tuple[list[PartySearchEntity], int]:
        query = query.strip()
        if not query:
            return [], 0

        fetch_limit = limit + offset
        legal_items = await self._unit_of_work.legal_entity_repository.list_all(
            limit=fetch_limit,
            offset=0,
            search=query,
        )
        individual_items = await self._unit_of_work.user_repository.search_individuals(
            query=query,
            limit=fetch_limit,
            offset=0,
        )
        legal_total = await self._unit_of_work.legal_entity_repository.count_all(search=query)
        individual_total = await self._unit_of_work.user_repository.count_individuals(query=query)
        items = [self._legal_to_search_entity(item) for item in legal_items] + individual_items
        items.sort(key=lambda item: item.created_at.timestamp() if item.created_at else 0, reverse=True)
        return items[offset:offset + limit], legal_total + individual_total

    def _legal_to_search_entity(self, item: LegalEntityEntity) -> PartySearchEntity:
        return PartySearchEntity(
            id=item.id,
            account_type=AccountType.LEGAL_ENTITY,
            user_id=item.user_id,
            email=None,
            name=item.name,
            inn=item.inn,
            phone=item.contact_phone,
            status=item.status,
            kyc_verified=item.kyc_verified,
            created_at=item.created_at,
        )
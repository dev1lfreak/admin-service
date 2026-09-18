from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Any

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.organization import PurchaseRequestEntity
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.database.decorators import transactional


VALID_STATUSES = frozenset({
    'submitted', 'in_review', 'quote_sent', 'payment_pending',
    'payment_received', 'usdt_sent', 'completed', 'rejected', 'cancelled',
})


class ListPurchaseRequestsCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(
        self,
        *,
        status: str | None = None,
        organization_id: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[PurchaseRequestEntity], int]:
        items = await self._unit_of_work.purchase_request_repository.list_all(
            status=status,
            organization_id=organization_id,
            limit=limit,
            offset=offset,
        )
        total = await self._unit_of_work.purchase_request_repository.count_all(
            status=status,
            organization_id=organization_id,
        )
        return items, total


class GetPurchaseRequestCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, request_id: str) -> PurchaseRequestEntity:
        return await self._unit_of_work.purchase_request_repository.get_by_id(request_id)


class CreatePurchaseRequestCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(
        self,
        *,
        organization_id: str,
        rub_amount: Decimal,
        status: str = 'submitted',
        usdt_amount: Decimal | None = None,
        exchange_rate: Decimal | None = None,
        service_fee_percent: Decimal | None = None,
        comment: str | None = None,
        admin_comment: str | None = None,
        target_wallet_chain: str | None = 'ETH',
        target_wallet_address: str | None = None,
        tx_hash: str | None = None,
        assigned_to: str | None = None,
    ) -> PurchaseRequestEntity:
        if status not in VALID_STATUSES:
            raise ApplicationException(status_code=400, message='Invalid status')

        await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)
        values: dict[str, Any] = {
            'organization_id': organization_id,
            'status': status,
            'rub_amount': rub_amount,
            'usdt_amount': usdt_amount,
            'exchange_rate': exchange_rate,
            'service_fee_percent': service_fee_percent,
            'comment': comment,
            'admin_comment': admin_comment,
            'target_wallet_chain': target_wallet_chain,
            'target_wallet_address': target_wallet_address,
            'tx_hash': tx_hash,
            'assigned_to': assigned_to,
        }
        if status == 'completed':
            values['completed_at'] = datetime.now(timezone.utc)

        created = await self._unit_of_work.purchase_request_repository.create(values)
        self._logger.info(f'Purchase request created id={created.id} org={organization_id}')
        return created


class UpdatePurchaseRequestStatusCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(
        self,
        request_id: str,
        *,
        status: str,
        admin_comment: str | None = None,
        assigned_to: str | None = None,
        tx_hash: str | None = None,
    ) -> PurchaseRequestEntity:
        if status not in VALID_STATUSES:
            raise ApplicationException(status_code=400, message='Invalid status')

        values: dict[str, Any] = {'status': status}
        if admin_comment is not None:
            values['admin_comment'] = admin_comment
        if assigned_to is not None:
            values['assigned_to'] = assigned_to
        if tx_hash is not None:
            values['tx_hash'] = tx_hash
        if status == 'completed':
            values['completed_at'] = datetime.now(timezone.utc)
        else:
            values['completed_at'] = None

        return await self._unit_of_work.purchase_request_repository.update(request_id, values=values)


class UpdatePurchaseRequestCommand:
    ALLOWED_FIELDS = frozenset({
        'status',
        'usdt_amount',
        'rub_amount',
        'exchange_rate',
        'service_fee_percent',
        'comment',
        'admin_comment',
        'target_wallet_chain',
        'target_wallet_address',
        'tx_hash',
        'assigned_to',
    })

    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, request_id: str, *, values: dict[str, Any]) -> PurchaseRequestEntity:
        filtered = {k: v for k, v in values.items() if k in self.ALLOWED_FIELDS}
        status = filtered.get('status')
        if status is not None:
            if status not in VALID_STATUSES:
                raise ApplicationException(status_code=400, message='Invalid status')
            if status == 'completed':
                filtered['completed_at'] = datetime.now(timezone.utc)
            else:
                filtered['completed_at'] = None

        return await self._unit_of_work.purchase_request_repository.update(request_id, values=filtered)


class SetPurchaseRequestQuoteCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(
        self,
        request_id: str,
        *,
        rub_amount: Decimal,
        exchange_rate: Decimal,
        service_fee_percent: Decimal | None = None,
        admin_comment: str | None = None,
    ) -> PurchaseRequestEntity:
        values: dict[str, Any] = {
            'rub_amount': rub_amount,
            'exchange_rate': exchange_rate,
            'status': 'quote_sent',
        }
        if service_fee_percent is not None:
            values['service_fee_percent'] = service_fee_percent
        if admin_comment is not None:
            values['admin_comment'] = admin_comment
        return await self._unit_of_work.purchase_request_repository.update(request_id, values=values)

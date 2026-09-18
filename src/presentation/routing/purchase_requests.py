from fastapi import APIRouter, Depends, Query, status

from src.application.commands import (
    CreatePurchaseRequestCommand,
    GetPurchaseRequestCommand,
    ListPurchaseRequestsCommand,
    SetPurchaseRequestQuoteCommand,
    UpdatePurchaseRequestCommand,
    UpdatePurchaseRequestStatusCommand,
)
from src.application.domain.dto import AdminAuthContext
from src.presentation.decorators.admin_auth import require_admin_access, require_admin_role
from src.presentation.dependencies.commands import (
    get_create_purchase_request_command,
    get_get_purchase_request_command,
    get_list_purchase_requests_command,
    get_set_purchase_request_quote_command,
    get_update_purchase_request_command,
    get_update_purchase_request_status_command,
)
from src.presentation.schemas.mappers import purchase_request_to_response
from src.presentation.schemas.entity import (
    CreatePurchaseRequestBody,
    PurchaseRequestListResponse,
    PurchaseRequestResponse,
    SetPurchaseRequestQuoteBody,
    UpdatePurchaseRequestBody,
    UpdatePurchaseRequestStatusBody,
)

purchase_requests_router = APIRouter(prefix='/purchase-requests', tags=['purchase-requests'])


@purchase_requests_router.get('', response_model=PurchaseRequestListResponse)
async def list_purchase_requests(
    status_filter: str | None = Query(default=None, alias='status'),
    organization_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListPurchaseRequestsCommand = Depends(get_list_purchase_requests_command),
):
    items, total = await command(
        status=status_filter,
        organization_id=organization_id,
        limit=limit,
        offset=offset,
    )
    return PurchaseRequestListResponse(
        items=[purchase_request_to_response(x) for x in items],
        total=total,
    )


@purchase_requests_router.post('', response_model=PurchaseRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_purchase_request(
    body: CreatePurchaseRequestBody,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: CreatePurchaseRequestCommand = Depends(get_create_purchase_request_command),
):
    item = await command(
        organization_id=body.organization_id,
        rub_amount=body.rub_amount,
        status=body.status,
        usdt_amount=body.usdt_amount,
        exchange_rate=body.exchange_rate,
        service_fee_percent=body.service_fee_percent,
        comment=body.comment,
        admin_comment=body.admin_comment,
        target_wallet_chain=body.target_wallet_chain,
        target_wallet_address=body.target_wallet_address,
        tx_hash=body.tx_hash,
        assigned_to=body.assigned_to,
    )
    return purchase_request_to_response(item)


@purchase_requests_router.get('/{request_id}', response_model=PurchaseRequestResponse)
async def get_purchase_request(
    request_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetPurchaseRequestCommand = Depends(get_get_purchase_request_command),
):
    item = await command(request_id)
    return purchase_request_to_response(item)


@purchase_requests_router.patch('/{request_id}', response_model=PurchaseRequestResponse)
async def update_purchase_request(
    request_id: str,
    body: UpdatePurchaseRequestBody,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: UpdatePurchaseRequestCommand = Depends(get_update_purchase_request_command),
):
    item = await command(request_id, values=body.model_dump(exclude_unset=True))
    return purchase_request_to_response(item)


@purchase_requests_router.patch('/{request_id}/status', response_model=PurchaseRequestResponse)
async def update_purchase_request_status(
    request_id: str,
    body: UpdatePurchaseRequestStatusBody,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: UpdatePurchaseRequestStatusCommand = Depends(get_update_purchase_request_status_command),
):
    item = await command(
        request_id,
        status=body.status,
        admin_comment=body.admin_comment,
        assigned_to=body.assigned_to,
        tx_hash=body.tx_hash,
    )
    return purchase_request_to_response(item)


@purchase_requests_router.post('/{request_id}/quote', response_model=PurchaseRequestResponse)
async def set_purchase_request_quote(
    request_id: str,
    body: SetPurchaseRequestQuoteBody,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: SetPurchaseRequestQuoteCommand = Depends(get_set_purchase_request_quote_command),
):
    item = await command(
        request_id,
        rub_amount=body.rub_amount,
        exchange_rate=body.exchange_rate,
        service_fee_percent=body.service_fee_percent,
        admin_comment=body.admin_comment,
    )
    return purchase_request_to_response(item)

from fastapi import APIRouter, Depends, Query

from src.application.domain.dto import AdminAuthContext
from src.presentation.decorators.admin_auth import require_admin_access, require_admin_role
from src.presentation.dependencies.commands import (
    get_list_orders_command,
    get_list_orders_by_date_command,
    get_get_order_command,
)
from src.presentation.schemas.mappers import order_to_response
from src.presentation.schemas.order import (
    OrdersResponse,
    OrdersByDateResponse,
    OrderDetailResponse,
)
from src.application.commands.orders_commands import (
    ListOrdersCommand,
    ListOrdersByDateCommand,
    GetOrderCommand,
)


orders_router = APIRouter(prefix='/orders', tags=['orders'])

@orders_router.get('', response_model=OrdersResponse)
async def list_orders(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    q: str | None = Query(default=None, min_length=1, max_length=255),
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListOrdersCommand = Depends(get_list_orders_command),
):
    items, total = await command(limit=limit, offset=offset, search=q)
    return OrdersResponse(
        items=[order_to_response(x) for x in items],
        total=total,
    )


@orders_router.get('/{order_id}', response_model=OrderDetailResponse)
async def get_order(
    order_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrderCommand = Depends(get_get_order_command),
):
    order = await command(order_id=order_id)
    return OrderDetailResponse(
        id=order.id,
        created_at=order.created_at.isoformat() if order.created_at is not None else None,
        updated_at=order.updated_at.isoformat() if order.updated_at is not None else None,
        user_id=order.user_id,
        usdt_amount=str(order.usdt_amount) if order.usdt_amount is not None else None,
        usdt_exchange_rate=str(order.usdt_exchange_rate) if order.usdt_exchange_rate is not None else None,
        gas_fee=str(order.gas_fee) if order.gas_fee is not None else None,
        total_price=str(order.total_price) if order.total_price is not None else None,
        service_fee=str(order.service_fee) if order.service_fee is not None else None,
        status=order.status,
        client_payment_id=order.client_payment_id,
        itpay_payment_qr_url_desktop=order.itpay_payment_qr_url_desktop,
        itpay_payment_qr_url_android=order.itpay_payment_qr_url_android,
        itpay_payment_qr_url_ios=order.itpay_payment_qr_url_ios,
        itpay_payment_qr_image_desktop=order.itpay_payment_qr_image_desktop,
        itpay_payment_qr_image_android=order.itpay_payment_qr_image_android,
        itpay_payment_qr_image_ios=order.itpay_payment_qr_image_ios,
        itpay_id=order.itpay_id,
        itpay_qr_id=order.itpay_qr_id,
        itpay_amount=str(order.itpay_amount) if order.itpay_amount is not None else None,
        itpay_created_at=order.itpay_created_at.isoformat() if order.itpay_created_at is not None else None,
    )


@orders_router.get('/filter/date', response_model=OrdersByDateResponse)
async def list_orders_by_date(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListOrdersByDateCommand = Depends(get_list_orders_by_date_command),
):
    orders, total, summary = await command(year=year, month=month, limit=limit, offset=offset)
    return OrdersByDateResponse(
        items=[order_to_response(o) for o in orders],
        total=total,
        summed_service_fees=summary,
    )

from fastapi import APIRouter, Depends, Request, Query, status

from src.application.domain.dto import AdminAuthContext
from src.presentation.decorators.admin_auth import require_admin_access
from src.presentation.dependencies.commands import (
    get_get_purchase_analytics_for_year_command,
    get_get_orders_analytics_for_year_command,
    get_get_purchase_analytics_for_month_command,
    get_get_orders_analytics_for_month_command,
    get_get_purchase_analytics_for_week_command,
    get_get_orders_analytics_for_week_command,
)
from src.presentation.schemas.analytics import (
    OrderAnalyticsResponse,
    PurchaseRequestAnalyticsResponse,
)
from src.application.commands.analytics_commands import (
    GetPurchaseAnalyticsForYearCommand,
    GetOrdersAnalyticsForYearCommand,
    GetPurchaseAnalyticsForMonthCommand,
    GetOrdersAnalyticsForMonthCommand,
    GetPurchaseAnalyticsForWeekCommand,
    GetOrdersAnalyticsForWeekCommand,
)

analytics_router = APIRouter(prefix='/analytics', tags=['analytics'])

@analytics_router.get('/purchases/yearly', response_model=PurchaseRequestAnalyticsResponse)
async def get_purchase_analytics_for_year(
    start_year: int = Query(..., ge=2000, le=2100),
    start_month: int = Query(..., ge=1, le=12),
    auth: AdminAuthContext = Depends(require_admin_access),
    status: str | None = Query(default=None, min_length=1, max_length=255),
    organization_id: str | None = Query(default=None, min_length=1, max_length=255),
    command: GetPurchaseAnalyticsForYearCommand = Depends(get_get_purchase_analytics_for_year_command),
):
    items, total, period = await command(
        start_year=start_year,
        start_month=start_month,
        status=status,
        organization_id=organization_id,
    )
    return PurchaseRequestAnalyticsResponse(
        requests_count=items,
        total_requests=total,
        period=period,
    )

@analytics_router.get('/orders/yearly', response_model=OrderAnalyticsResponse)
async def get_orders_analytics_for_year(
    start_year: int = Query(..., ge=2000, le=2100),
    start_month: int = Query(..., ge=1, le=12),
    auth: AdminAuthContext = Depends(require_admin_access),
    q: str | None = Query(default=None, min_length=1, max_length=255),
    command: GetOrdersAnalyticsForYearCommand = Depends(get_get_orders_analytics_for_year_command),
):
    orders_count, orders_sum, total_orders, total_sum, period = await command(
        start_year=start_year,
        start_month=start_month,
        search=q,
    )
    return OrderAnalyticsResponse(
        orders_count=orders_count,
        summed_service_fees=orders_sum,
        total_orders=total_orders,
        total_summed_service_fees=total_sum,
        period=period,
    )

@analytics_router.get('/purchases/monthly', response_model=PurchaseRequestAnalyticsResponse)
async def get_purchase_analytics_for_month(
    start_year: int = Query(..., ge=2000, le=2100),
    start_month: int = Query(..., ge=1, le=12),
    start_day: int = Query(..., ge=1, le=31),
    auth: AdminAuthContext = Depends(require_admin_access),
    status: str | None = Query(default=None, min_length=1, max_length=255),
    organization_id: str | None = Query(default=None, min_length=1, max_length=255),
    command: GetPurchaseAnalyticsForMonthCommand = Depends(get_get_purchase_analytics_for_month_command),
):
    items, total, period = await command(
        start_year=start_year,
        start_month=start_month,
        start_day=start_day,
        status=status,
        organization_id=organization_id,
    )
    return PurchaseRequestAnalyticsResponse(
        requests_count=items,
        total_requests=total,
        period=period,
    )

@analytics_router.get('/orders/monthly', response_model=OrderAnalyticsResponse)
async def get_orders_analytics_for_month(
    start_year: int = Query(..., ge=2000, le=2100),
    start_month: int = Query(..., ge=1, le=12),
    start_day: int = Query(..., ge=1, le=31),
    auth: AdminAuthContext = Depends(require_admin_access),
    q: str | None = Query(default=None, min_length=1, max_length=255),
    command: GetOrdersAnalyticsForMonthCommand = Depends(get_get_orders_analytics_for_month_command),
):
    orders_count, orders_sum, total_orders, total_sum, period = await command(
        start_year=start_year,
        start_month=start_month,
        start_day=start_day,
        search=q,
    )
    return OrderAnalyticsResponse(
        orders_count=orders_count,
        summed_service_fees=orders_sum,
        total_orders=total_orders,
        total_summed_service_fees=total_sum,
        period=period,
    )

@analytics_router.get('/purchases/weekly', response_model=PurchaseRequestAnalyticsResponse)
async def get_purchase_analytics_for_week(
    start_year: int = Query(..., ge=2000, le=2100),
    start_month: int = Query(..., ge=1, le=12),
    start_day: int = Query(..., ge=1, le=31),
    auth: AdminAuthContext = Depends(require_admin_access),
    status: str | None = Query(default=None, min_length=1, max_length=255),
    organization_id: str | None = Query(default=None, min_length=1, max_length=255),
    command: GetPurchaseAnalyticsForWeekCommand = Depends(get_get_purchase_analytics_for_week_command),
):
    items, total, period = await command(
        start_year=start_year,
        start_month=start_month,
        start_day=start_day,
        status=status,
        organization_id=organization_id,
    )
    return PurchaseRequestAnalyticsResponse(
        requests_count=items,
        total_requests=total,
        period=period,
    )

@analytics_router.get('/orders/weekly', response_model=OrderAnalyticsResponse)
async def get_orders_analytics_for_week(
    start_year: int = Query(..., ge=2000, le=2100),
    start_month: int = Query(..., ge=1, le=12),
    start_day: int = Query(..., ge=1, le=31),
    auth: AdminAuthContext = Depends(require_admin_access),
    q: str | None = Query(default=None, min_length=1, max_length=255),
    command: GetOrdersAnalyticsForWeekCommand = Depends(get_get_orders_analytics_for_week_command),
):
    orders_count, orders_sum, total_orders, total_sum, period = await command(
        start_year=start_year,
        start_month=start_month,
        start_day=start_day,
        search=q,
    )
    return OrderAnalyticsResponse(
        orders_count=orders_count,
        summed_service_fees=orders_sum,
        total_orders=total_orders,
        total_summed_service_fees=total_sum,
        period=period,
    )
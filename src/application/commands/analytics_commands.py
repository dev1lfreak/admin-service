from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from datetime import date, timedelta

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities import OrderEntity, PurchaseRequestEntity
from src.application.domain.exceptions import NotFoundException
from src.infrastructure.database.decorators import transactional


YEAR=12
MONTH=30
WEEK=7

def _count_date(
    year: int,
    month: int | None = None,
    day: int | None = None,
) -> tuple[int, int | None, int | None]:
    if month is None:
        return year - 1, None, None

    if day is None:
        return (year - 1, 12, None) if month == 1 else (year, month - 1, None)

    prev_date = date(year, month, day) - timedelta(days=1)
    return prev_date.year, prev_date.month, prev_date.day


class GetOrdersAnalyticsForYearCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(
        self, 
        *, 
        start_year: int, 
        start_month: int | None = None,
        search: str | None = None,
    ) -> tuple[list[int], list[Decimal], int, Decimal, int]:
        orders: list[int] = []
        sums: list[Decimal] = []
        year, month = start_year, start_month

        for _ in range(YEAR):
            order_count = await self._unit_of_work.order_repository.count_by_month(
                    year=year,
                    month=month,
                    search=search,
                )
            order_sum = await self._unit_of_work.order_repository.sum_by_month(
                    year=year,
                    month=month,
                    search=search,
                )
    
            orders.append(order_count)
            sums.append(order_sum)
            year, month, _ = _count_date(year, month)
        return orders, sums, sum(orders), sum(sums), YEAR


class GetPurchaseAnalyticsForYearCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(
        self, 
        *, 
        start_year: int, 
        start_month: int | None = None,
        status: str | None = None,
        organization_id: str | None = None,
    ) -> tuple[list[int], int, int]:
        requests: list[int] = []
        year, month = start_year, start_month

        for _ in range(YEAR):
            request_count = await self._unit_of_work.purchase_request_repository.count_for_month(
                    year=year,
                    month=month,
                    status=status,
                    organization_id=organization_id,
                )
            requests.append(request_count)
            year, month, _ = _count_date(year, month)
        return requests, sum(requests), YEAR
    

class GetOrdersAnalyticsForMonthCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(
        self, 
        *, 
        start_year: int, 
        start_month: int,
        start_day: int | None = None,
        search: str | None = None,
    ) -> tuple[list[int], list[Decimal], int, Decimal, int]:
        orders: list[int] = []
        sums: list[Decimal] = []
        year, month, day = start_year, start_month, start_day

        for _ in range(MONTH):
            order_count = await self._unit_of_work.order_repository.count_by_day(
                    year=year,
                    month=month,
                    day=day,
                    search=search,
                )
            order_sum = await self._unit_of_work.order_repository.sum_by_day(
                    year=year,
                    month=month,
                    day=day,
                    search=search,
                )
    
            orders.append(order_count)
            sums.append(order_sum)
            year, month, day = _count_date(year, month, day)
        return orders, sums, sum(orders), sum(sums), MONTH


class GetPurchaseAnalyticsForMonthCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(
        self, 
        *, 
        start_year: int, 
        start_month: int,
        start_day: int | None = None,
        status: str | None = None,
        organization_id: str | None = None,
    ) -> tuple[list[PurchaseRequestEntity], int, int]:
        requests: list[int] = []
        year, month, day = start_year, start_month, start_day

        for _ in range(MONTH):
            request_count = await self._unit_of_work.purchase_request_repository.count_for_day(
                    year=year,
                    month=month,
                    day=day,
                    status=status,
                    organization_id=organization_id,
                )
            
            requests.append(request_count)
            year, month, day = _count_date(year, month, day)
        return requests, sum(requests), MONTH


class GetPurchaseAnalyticsForWeekCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(
        self, 
        *, 
        start_year: int, 
        start_month: int, 
        start_day: int,
        status: str | None = None,
        organization_id: str | None = None,
    ) -> tuple[list[PurchaseRequestEntity], int, int]:
        requests: list[int] = []
        year, month, day = start_year, start_month, start_day

        for _ in range(WEEK):
            request_count = await self._unit_of_work.purchase_request_repository.count_for_day(
                    year=year,
                    month=month,
                    day=day,
                    status=status,
                    organization_id=organization_id,
                )
            
            requests.append(request_count)
            year, month, day = _count_date(year, month, day)
        return requests, sum(requests), WEEK


class GetOrdersAnalyticsForWeekCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(
        self, 
        *,  
        start_year: int, 
        start_month: int, 
        start_day: int,
        search: str | None = None,
    ) -> tuple[list[OrderEntity], int, Decimal, int]:
        orders: list[int] = []
        sums: list[Decimal] = []
        year, month, day = start_year, start_month, start_day

        for _ in range(WEEK):
            order_count = await self._unit_of_work.order_repository.count_by_day(
                    year=year,
                    month=month,
                    day=day,
                    search=search,
                )
            order_sum = await self._unit_of_work.order_repository.sum_by_day(
                    year=year,
                    month=month,
                    day=day,
                    search=search,
                )
    
            orders.append(order_count)
            sums.append(order_sum)
            year, month, day = _count_date(year, month, day)
        return orders, sums, sum(orders), sum(sums), WEEK
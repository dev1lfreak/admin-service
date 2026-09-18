from __future__ import annotations
from decimal import Decimal
from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities import OrderEntity
from src.application.domain.exceptions import NotFoundException
from src.infrastructure.database.decorators import transactional


class ListUserOrdersCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(self, *, user_id: str, limit: int, offset: int) -> tuple[list[OrderEntity], int]:
        orders = await self._unit_of_work.order_repository.list_by_user_id(
            user_id=user_id,
            limit=limit,
            offset=offset,
        )
        total = await self._unit_of_work.order_repository.count_all(search=user_id)
        return orders, total

    
    
class ListOrdersCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(self, *, limit: int, offset: int, search: str | None = None) -> tuple[list[OrderEntity], int]:
        orders = await self._unit_of_work.order_repository.list_all(
            limit=limit,
            offset=offset,
            search=search
        )

        total = await self._unit_of_work.order_repository.count_all(search=search)

        return orders, total


class ListOrdersByDateCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(
        self, 
        *, 
        limit: int, 
        offset: int, 
        year: int, 
        month: int | None = None
    ) -> tuple[list[OrderEntity], int, Decimal]:
        orders = await self._unit_of_work.order_repository.list_by_date(
            year=year,
            month=month,
            limit=limit,
            offset=offset
        )

        total = await self._unit_of_work.order_repository.count_by_month(year=year, month=month)
        summary = await self._unit_of_work.order_repository.sum_by_month(year=year, month=month)

        return orders, total, summary


class GetOrderCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger


    @transactional
    async def __call__(self, *, order_id: str) -> OrderEntity:
        order = await self._unit_of_work.order_repository.get_by_id(order_id=order_id)
        if order is None:
            raise NotFoundException(message='Order not found')
        
        return order

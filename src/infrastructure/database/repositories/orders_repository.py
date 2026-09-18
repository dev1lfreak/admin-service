from __future__ import annotations
from dataclasses import replace
from decimal import Decimal
from sqlalchemy import desc, select, or_, extract, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.abstractions.repositories.i_order_repository import IOrderRepository
from src.application.contracts import ILogger
from src.application.domain.entities.order import OrderEntity
from src.application.domain.enums import OrderStatus
from src.infrastructure.database.models.order import OrderModel


class OrderRepository(IOrderRepository):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self._session = session
        self._logger = logger


    @staticmethod
    def _to_entity(model: OrderModel) -> OrderEntity:
        return OrderEntity(
            id=model.id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            user_id=model.user_id,
            usdt_amount=model.usdt_amount,
            usdt_exchange_rate=model.usdt_exchange_rate,
            gas_fee=model.gas_fee,
            total_price=model.total_price,
            service_fee=model.service_fee,
            status=model.status,
            client_payment_id=model.client_payment_id,
            itpay_payment_qr_url_desktop=model.itpay_payment_qr_url_desktop,
            itpay_payment_qr_url_android=model.itpay_payment_qr_url_android,
            itpay_payment_qr_url_ios=model.itpay_payment_qr_url_ios,
            itpay_payment_qr_image_desktop=model.itpay_payment_qr_image_desktop,
            itpay_payment_qr_image_android=model.itpay_payment_qr_image_android,
            itpay_payment_qr_image_ios=model.itpay_payment_qr_image_ios,
            itpay_id=model.itpay_id,
            itpay_qr_id=model.itpay_qr_id,
            itpay_amount=model.itpay_amount,
            itpay_created_at=model.itpay_created_at,
        )
    
    
    def _search_filter(self, search: str | None):
        if not search or not search.strip():
            return None

        pattern = f'%{search.strip()}%'
        return or_(
            OrderModel.id.ilike(pattern),
            OrderModel.user_id.ilike(pattern),
            OrderModel.status.ilike(pattern),
            OrderModel.client_payment_id.ilike(pattern),
            OrderModel.itpay_id.ilike(pattern),
            OrderModel.itpay_qr_id.ilike(pattern),
        )


    async def get_by_id(self,order_id: str) -> OrderEntity | None:
        stmt=select(OrderModel).where(OrderModel.id==order_id)
        model=await self._session.scalar(stmt)
        if model is None:
            return None
        return self._to_entity(model)


    async def list_by_user_id(
            self,
            *,
            user_id: str,
            limit: int,
            offset: int
    ) -> list[OrderEntity]:
        stmt=(
            select(OrderModel)
            .where(OrderModel.user_id==user_id)
            .order_by(desc(OrderModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        result=await self._session.scalars(stmt)
        return [self._to_entity(model) for model in result.all()]


    async def list_all(
            self,
            *,
            limit: int,
            offset: int,
            search: str | None = None
    ) -> list[OrderEntity]:
        stmt=(
            select(OrderModel)
            .order_by(desc(OrderModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return [self._to_entity(model) for model in res.scalars().all()]


    async def list_by_date(
            self,
            *,
            year: int,
            month: int,
            limit: int,
            offset: int,
    ) -> list[OrderEntity]:
        stmt=(
            select(OrderModel)
            .where(
                extract("year", OrderModel.created_at) == year,
                extract("month", OrderModel.created_at) == month,
            )
            .order_by(desc(OrderModel.created_at))
            .limit(limit)
            .offset(offset)
        )
        res = await self._session.execute(stmt)
        return [self._to_entity(model) for model in res.scalars().all()]
    

    async def sum_by_month(
            self, 
            *, 
            year: int, 
            month: int, 
            search: str | None = None,
    ) -> Decimal:
        stmt = (
            select(func.coalesce(func.sum(OrderModel.service_fee), 0))
            .where(
                extract("year", OrderModel.created_at) == year,
                extract("month", OrderModel.created_at) == month,
                OrderModel.status == OrderStatus.COMPLETED.value,
            )
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return res.scalar_one()
    

    async def sum_by_day(
            self, 
            *, 
            year: int, 
            month: int, 
            day: int,
            search: str | None = None,
    ) -> Decimal:
        stmt = (
            select(func.coalesce(func.sum(OrderModel.service_fee), 0))
            .where(
                extract("year", OrderModel.created_at) == year,
                extract("month", OrderModel.created_at) == month,
                extract("day", OrderModel.created_at) == day,
                OrderModel.status == OrderStatus.COMPLETED.value,
            )
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return res.scalar_one()
    

    async def count_all(self,*,search: str | None = None) -> int:
        stmt = select(func.count()).select_from(OrderModel)
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return int(res.scalar_one())
    

    async def count_by_month(self,*,year: int,month: int, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(OrderModel)
        stmt = stmt.where(
                extract("year", OrderModel.created_at) == year,
                extract("month", OrderModel.created_at) == month
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return int(res.scalar_one())
    

    async def count_by_day(self,*,year: int,month: int,day: int, search: str | None = None) -> int:
        stmt = select(func.count()).select_from(OrderModel)
        stmt = stmt.where(
                extract("year", OrderModel.created_at) == year,
                extract("month", OrderModel.created_at) == month,
                extract("day", OrderModel.created_at) == day
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return int(res.scalar_one())

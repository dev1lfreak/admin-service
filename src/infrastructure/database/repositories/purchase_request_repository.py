from __future__ import annotations

from typing import Any

from ulid import ULID
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.application.abstractions.repositories import IPurchaseRequestRepository
from src.application.contracts import ILogger
from src.application.domain.entities.organization import PurchaseRequestEntity
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.database.models import PurchaseRequestModel


class PurchaseRequestRepository(IPurchaseRequestRepository):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self._session = session
        self._logger = logger

    def _to_entity(self, m: PurchaseRequestModel) -> PurchaseRequestEntity:
        return PurchaseRequestEntity(
            id=m.id,
            organization_id=m.organization_id,
            status=m.status,
            usdt_amount=m.usdt_amount,
            rub_amount=m.rub_amount,
            exchange_rate=m.exchange_rate,
            service_fee_percent=m.service_fee_percent,
            comment=m.comment,
            admin_comment=m.admin_comment,
            target_wallet_chain=m.target_wallet_chain,
            target_wallet_address=m.target_wallet_address,
            tx_hash=m.tx_hash,
            assigned_to=m.assigned_to,
            created_at=m.created_at,
            updated_at=m.updated_at,
            completed_at=m.completed_at,
        )

    def _apply_filters(self, stmt, *, status: str | None, organization_id: str | None):
        if status:
            stmt = stmt.where(PurchaseRequestModel.status == status)
        if organization_id:
            stmt = stmt.where(PurchaseRequestModel.organization_id == organization_id)
        return stmt

    async def create(self, values: dict[str, Any]) -> PurchaseRequestEntity:
        model = PurchaseRequestModel(id=str(ULID()), **values)
        self._session.add(model)
        try:
            await self._session.flush()
            return self._to_entity(model)
        except SQLAlchemyError as exc:
            self._logger.exception(str(exc))
            raise ApplicationException(status_code=500, message='Database error')

    async def get_by_id(self, request_id: str) -> PurchaseRequestEntity:
        res = await self._session.execute(select(PurchaseRequestModel).where(PurchaseRequestModel.id == request_id))
        m = res.scalar_one_or_none()
        if m is None:
            raise ApplicationException(status_code=404, message='Purchase request not found')
        return self._to_entity(m)

    async def list_all(
        self,
        *,
        status: str | None,
        organization_id: str | None,
        limit: int,
        offset: int,
    ) -> list[PurchaseRequestEntity]:
        stmt = select(PurchaseRequestModel).order_by(PurchaseRequestModel.created_at.desc())
        stmt = self._apply_filters(stmt, status=status, organization_id=organization_id)
        res = await self._session.execute(stmt.limit(limit).offset(offset))
        return [self._to_entity(m) for m in res.scalars().all()]

    async def count_all(self, *, status: str | None, organization_id: str | None) -> int:
        stmt = select(func.count()).select_from(PurchaseRequestModel)
        stmt = self._apply_filters(stmt, status=status, organization_id=organization_id)
        res = await self._session.execute(stmt)
        return int(res.scalar_one())

    async def update(self, request_id: str, *, values: dict[str, Any]) -> PurchaseRequestEntity:
        if not values:
            return await self.get_by_id(request_id)
        await self._session.execute(
            update(PurchaseRequestModel).where(PurchaseRequestModel.id == request_id).values(**values)
        )
        await self._session.flush()
        return await self.get_by_id(request_id)
    

    async def count_for_month(
            self,
            *, 
            year: int, 
            month: int,  
            status: str | None, 
            organization_id: str | None
    ) -> int:
        stmt = select(func.count()).select_from(PurchaseRequestModel)
        stmt = self._apply_filters(stmt, status=status, organization_id=organization_id)
        stmt = stmt.where(
            func.extract("year", PurchaseRequestModel.created_at) == year,
            func.extract("month", PurchaseRequestModel.created_at) == month,
        )
        res = await self._session.execute(stmt)
        return int(res.scalar_one())


    async def count_for_day(
            self, 
            *, 
            year: int, 
            month: int, 
            day: int, 
            status: str | None, 
            organization_id: str | None
    ) -> int:
        stmt = select(func.count()).select_from(PurchaseRequestModel)
        stmt = self._apply_filters(stmt, status=status, organization_id=organization_id)
        stmt = stmt.where(
            func.extract("year", PurchaseRequestModel.created_at) == year,
            func.extract("month", PurchaseRequestModel.created_at) == month,
            func.extract("day", PurchaseRequestModel.created_at) == day,
        )
        res = await self._session.execute(stmt)
        return int(res.scalar_one())

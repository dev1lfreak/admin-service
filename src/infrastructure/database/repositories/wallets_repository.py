from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.abstractions.repositories import IWalletRepository
from src.application.contracts import ILogger
from src.application.domain.entities.user import WalletEntity
from src.infrastructure.database.models import WalletModel


class WalletRepository(IWalletRepository):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self._session = session
        self._logger = logger

    def _to_entity(self, m: WalletModel) -> WalletEntity:
        return WalletEntity(
            id=m.id,
            user_id=m.user_id,
            chain=m.chain,
            address=m.address,
            derivation_path=m.derivation_path,
            created_at=m.created_at,
        )

    async def list_by_user(self, user_id: str) -> list[WalletEntity]:
        res = await self._session.execute(
            select(WalletModel)
            .where(WalletModel.user_id == user_id)
            .order_by(WalletModel.chain)
        )
        return [self._to_entity(m) for m in res.scalars().all()]

    async def exists_for_user(self, user_id: str) -> bool:
        res = await self._session.execute(
            select(WalletModel.id)
            .where(WalletModel.user_id == user_id)
            .limit(1)
        )
        return res.scalar_one_or_none() is not None

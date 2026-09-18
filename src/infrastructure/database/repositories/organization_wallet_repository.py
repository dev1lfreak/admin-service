from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.application.abstractions.repositories import IOrganizationWalletRepository
from src.application.contracts import ILogger
from src.application.domain.entities.organization import OrganizationWalletEntity
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.database.models import OrganizationWalletModel


class OrganizationWalletRepository(IOrganizationWalletRepository):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self._session = session
        self._logger = logger

    def _to_entity(self, m: OrganizationWalletModel) -> OrganizationWalletEntity:
        return OrganizationWalletEntity(
            id=m.id,
            organization_id=m.organization_id,
            chain=m.chain,
            address=m.address,
            derivation_path=m.derivation_path,
            created_at=m.created_at,
        )

    async def create_many(self, wallets: list[OrganizationWalletEntity]) -> list[OrganizationWalletEntity]:
        models = [
            OrganizationWalletModel(
                id=w.id,
                organization_id=w.organization_id,
                chain=w.chain,
                address=w.address,
                derivation_path=w.derivation_path,
            )
            for w in wallets
        ]
        self._session.add_all(models)
        try:
            await self._session.flush()
            return [self._to_entity(m) for m in models]
        except IntegrityError:
            raise ApplicationException(status_code=409, message='Wallets already exist for organization')
        except SQLAlchemyError as exc:
            self._logger.exception(str(exc))
            raise ApplicationException(status_code=500, message='Database error')

    async def list_by_organization(self, organization_id: str) -> list[OrganizationWalletEntity]:
        res = await self._session.execute(
            select(OrganizationWalletModel)
            .where(OrganizationWalletModel.organization_id == organization_id)
            .order_by(OrganizationWalletModel.chain)
        )
        return [self._to_entity(m) for m in res.scalars().all()]

    async def exists_for_organization(self, organization_id: str) -> bool:
        res = await self._session.execute(
            select(OrganizationWalletModel.id)
            .where(OrganizationWalletModel.organization_id == organization_id)
            .limit(1)
        )
        return res.scalar_one_or_none() is not None

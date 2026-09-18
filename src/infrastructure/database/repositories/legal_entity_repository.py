from __future__ import annotations

from typing import Any

from sqlalchemy import func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.application.abstractions.repositories import ILegalEntityRepository
from src.application.contracts import ILogger
from src.application.domain.entities.organization import LegalEntityEntity
from src.application.domain.exceptions import ApplicationException
from src.application.domain.organization_documents import DOCUMENT_TYPE_TO_COLUMN, ORGANIZATION_DOCUMENT_TYPES
from src.infrastructure.database.models import LegalEntityModel, UserModel


class LegalEntityRepository(ILegalEntityRepository):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self._session = session
        self._logger = logger

    def _document_s3_keys_from_model(self, m: LegalEntityModel) -> dict[str, str | None]:
        return {
            document_type: getattr(m, DOCUMENT_TYPE_TO_COLUMN[document_type])
            for document_type in ORGANIZATION_DOCUMENT_TYPES
        }

    def _to_entity(self, m: LegalEntityModel) -> LegalEntityEntity:
        return LegalEntityEntity(
            id=m.id,
            user_id=m.user_id,
            name=m.name,
            short_name=m.short_name,
            inn=m.inn,
            ogrn=m.ogrn,
            kpp=m.kpp,
            legal_address=m.legal_address,
            actual_address=m.actual_address,
            bank_details=m.bank_details,
            contact_person=m.contact_person,
            contact_phone=m.contact_phone,
            status=m.status,
            kyc_verified=m.kyc_verified,
            kyc_verified_at=m.kyc_verified_at,
            encrypted_mnemonic=m.encrypted_mnemonic,
            document_s3_keys=self._document_s3_keys_from_model(m),
            created_by=m.created_by,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )

    def _search_filter(self, search: str | None):
        if not search or not search.strip():
            return None

        pattern = f'%{search.strip()}%'
        full_name = func.concat_ws(
            ' ',
            UserModel.last_name,
            UserModel.first_name,
            UserModel.middle_name,
        )
        return or_(
            LegalEntityModel.id.ilike(pattern),
            LegalEntityModel.name.ilike(pattern),
            LegalEntityModel.short_name.ilike(pattern),
            LegalEntityModel.inn.ilike(pattern),
            LegalEntityModel.ogrn.ilike(pattern),
            LegalEntityModel.kpp.ilike(pattern),
            LegalEntityModel.legal_address.ilike(pattern),
            LegalEntityModel.actual_address.ilike(pattern),
            LegalEntityModel.contact_person.ilike(pattern),
            LegalEntityModel.contact_phone.ilike(pattern),
            UserModel.email.ilike(pattern),
            UserModel.last_name.ilike(pattern),
            UserModel.first_name.ilike(pattern),
            UserModel.middle_name.ilike(pattern),
            UserModel.phone.ilike(pattern),
            UserModel.inn.ilike(pattern),
            full_name.ilike(pattern),
        )

    async def create(
        self,
        *,
        user_id: str,
        name: str,
        short_name: str | None,
        inn: str,
        ogrn: str | None,
        kpp: str | None,
        legal_address: str | None,
        actual_address: str | None,
        bank_details: dict[str, Any] | None,
        contact_person: str | None,
        contact_phone: str | None,
        status: str,
        kyc_verified: bool,
        kyc_verified_at,
        created_by: str | None,
    ) -> LegalEntityEntity:
        entity = LegalEntityModel(
            user_id=user_id,
            name=name,
            short_name=short_name,
            inn=inn,
            ogrn=ogrn,
            kpp=kpp,
            legal_address=legal_address,
            actual_address=actual_address,
            bank_details=bank_details,
            contact_person=contact_person,
            contact_phone=contact_phone,
            status=status,
            kyc_verified=kyc_verified,
            kyc_verified_at=kyc_verified_at,
            created_by=created_by,
        )
        self._session.add(entity)
        try:
            await self._session.flush()
            return self._to_entity(entity)
        except IntegrityError:
            raise ApplicationException(status_code=409, message='Organization with this INN or user already exists')
        except SQLAlchemyError as exc:
            self._logger.exception(str(exc))
            raise ApplicationException(status_code=500, message='Database error')

    async def get_by_id(self, organization_id: str) -> LegalEntityEntity:
        res = await self._session.execute(select(LegalEntityModel).where(LegalEntityModel.id == organization_id))
        m = res.scalar_one_or_none()
        if m is None:
            raise ApplicationException(status_code=404, message='Organization not found')
        return self._to_entity(m)

    async def list_all(
        self,
        *,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> list[LegalEntityEntity]:
        stmt = (
            select(LegalEntityModel)
            .join(UserModel, UserModel.id == LegalEntityModel.user_id)
            .where(UserModel.is_deleted.is_(False))
            .order_by(LegalEntityModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return [self._to_entity(m) for m in res.scalars().all()]

    async def count_all(self, *, search: str | None = None) -> int:
        stmt = (
            select(func.count(LegalEntityModel.id))
            .join(UserModel, UserModel.id == LegalEntityModel.user_id)
            .where(UserModel.is_deleted.is_(False))
        )
        search_filter = self._search_filter(search)
        if search_filter is not None:
            stmt = stmt.where(search_filter)
        res = await self._session.execute(stmt)
        return int(res.scalar_one())

    async def update(self, organization_id: str, *, values: dict[str, Any]) -> LegalEntityEntity:
        if not values:
            return await self.get_by_id(organization_id)
        await self._session.execute(
            update(LegalEntityModel).where(LegalEntityModel.id == organization_id).values(**values)
        )
        await self._session.flush()
        return await self.get_by_id(organization_id)

    async def set_encrypted_mnemonic(self, organization_id: str, encrypted_mnemonic: str) -> None:
        await self._session.execute(
            update(LegalEntityModel)
            .where(LegalEntityModel.id == organization_id)
            .values(encrypted_mnemonic=encrypted_mnemonic)
        )
        await self._session.flush()

    async def get_document_s3_key(self, organization_id: str, document_type: str) -> str | None:
        org = await self.get_by_id(organization_id)
        return org.document_s3_keys.get(document_type)

    async def set_document_s3_key(self, organization_id: str, document_type: str, s3_key: str) -> LegalEntityEntity:
        column = DOCUMENT_TYPE_TO_COLUMN.get(document_type)
        if column is None:
            raise ApplicationException(status_code=400, message='Invalid document type')
        await self._session.execute(
            update(LegalEntityModel)
            .where(LegalEntityModel.id == organization_id)
            .values(**{column: s3_key})
        )
        await self._session.flush()
        return await self.get_by_id(organization_id)

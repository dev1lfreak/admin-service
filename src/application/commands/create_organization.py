from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.application.abstractions import IUnitOfWork
from src.application.contracts import IHashService, ILogger
from src.application.domain.entities.organization import LegalEntityEntity
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.database.decorators import transactional


class CreateOrganizationCommand:
    def __init__(self, unit_of_work: IUnitOfWork, hash_service: IHashService, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._hash_service = hash_service
        self._logger = logger

    @transactional
    async def __call__(
        self,
        *,
        admin_user_id: str,
        email: str,
        password: str,
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
        status: str = 'active',
    ) -> LegalEntityEntity:
        email = (email or '').strip().lower()
        if await self._unit_of_work.user_repository.exists_by_email(email):
            raise ApplicationException(status_code=409, message='User with this email already exists')

        now = datetime.now(timezone.utc)
        password_hash = await self._hash_service.hash(value=password)
        user = await self._unit_of_work.user_repository.create_legal_entity_user(
            email=email,
            password_hash=password_hash,
            provisioned_by=admin_user_id,
            provisioned_at=now,
            kyc_verified=True,
            kyc_verified_at=now,
        )

        org = await self._unit_of_work.legal_entity_repository.create(
            user_id=user.id,
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
            kyc_verified=True,
            kyc_verified_at=now,
            created_by=admin_user_id,
        )
        self._logger.info(f'Organization created id={org.id} user_id={user.id}')
        return org

from abc import ABC, abstractmethod
from typing import Any

from src.application.domain.entities.organization import LegalEntityEntity


class ILegalEntityRepository(ABC):
    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, organization_id: str) -> LegalEntityEntity:
        raise NotImplementedError

    @abstractmethod
    async def list_all(self, *, limit: int, offset: int, search: str | None = None) -> list[LegalEntityEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        organization_id: str,
        *,
        values: dict[str, Any],
    ) -> LegalEntityEntity:
        raise NotImplementedError

    @abstractmethod
    async def set_encrypted_mnemonic(self, organization_id: str, encrypted_mnemonic: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_document_s3_key(self, organization_id: str, document_type: str) -> str | None:
        raise NotImplementedError

    @abstractmethod
    async def set_document_s3_key(self, organization_id: str, document_type: str, s3_key: str) -> LegalEntityEntity:
        raise NotImplementedError

    @abstractmethod
    async def count_all(self, *, search: str | None = None) -> int:
        raise NotImplementedError

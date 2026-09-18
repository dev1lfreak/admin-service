from __future__ import annotations

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.organization import LegalEntityEntity, OrganizationWalletEntity
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.crypto.wallet_crypto import (
    DerivedSecretKey,
    decrypt_mnemonic,
    derive_all_private_keys,
    is_crypto_ready,
)
from src.infrastructure.database.decorators import transactional


class ListOrganizationWalletsCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, organization_id: str) -> list[OrganizationWalletEntity]:
        await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)
        return await self._unit_of_work.organization_wallet_repository.list_by_organization(organization_id)


class GetOrganizationMnemonicCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, organization_id: str) -> str:
        org = await self._require_wallets_org(organization_id)
        if not is_crypto_ready():
            raise ApplicationException(status_code=503, message='Crypto service not ready')
        return decrypt_mnemonic(org.encrypted_mnemonic or '')

    async def _require_wallets_org(self, organization_id: str) -> LegalEntityEntity:
        org = await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)
        if not org.encrypted_mnemonic:
            raise ApplicationException(status_code=404, message='Wallets not created for organization')
        return org


class GetOrganizationSecretKeysCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, organization_id: str) -> list[DerivedSecretKey]:
        org = await self._require_wallets_org(organization_id)
        if not is_crypto_ready():
            raise ApplicationException(status_code=503, message='Crypto service not ready')
        mnemonic = decrypt_mnemonic(org.encrypted_mnemonic or '')
        return derive_all_private_keys(mnemonic)

    async def _require_wallets_org(self, organization_id: str) -> LegalEntityEntity:
        org = await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)
        if not org.encrypted_mnemonic:
            raise ApplicationException(status_code=404, message='Wallets not created for organization')
        return org

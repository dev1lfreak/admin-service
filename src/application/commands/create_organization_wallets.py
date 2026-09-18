from __future__ import annotations

from ulid import ULID

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.organization import (
    CreateOrganizationWalletsResult,
    OrganizationWalletEntity,
)
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.crypto.wallet_crypto import (
    ALL_CHAINS,
    derive_all_addresses,
    encrypt_mnemonic,
    generate_mnemonic,
    is_crypto_ready,
)
from src.infrastructure.database.decorators import transactional


class CreateOrganizationWalletsCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, *, organization_id: str) -> CreateOrganizationWalletsResult:
        if not is_crypto_ready():
            raise ApplicationException(status_code=503, message='Crypto service not ready')

        org = await self._unit_of_work.legal_entity_repository.get_by_id(organization_id)
        if org.encrypted_mnemonic:
            raise ApplicationException(status_code=409, message='Wallets already created for organization')

        if await self._unit_of_work.organization_wallet_repository.exists_for_organization(organization_id):
            raise ApplicationException(status_code=409, message='Wallets already exist for organization')

        mnemonic = generate_mnemonic()
        derived = derive_all_addresses(mnemonic)
        plaintext_mnemonic = mnemonic
        blob = encrypt_mnemonic(mnemonic)
        mnemonic = ''

        await self._unit_of_work.legal_entity_repository.set_encrypted_mnemonic(organization_id, blob)

        wallets = [
            OrganizationWalletEntity(
                id=str(ULID()),
                organization_id=organization_id,
                chain=item.chain,
                address=item.address,
                derivation_path=item.derivation_path,
            )
            for item in derived
            if item.chain in ALL_CHAINS
        ]
        saved = await self._unit_of_work.organization_wallet_repository.create_many(wallets)
        self._logger.info(f'Wallets created for organization_id={organization_id} chains={len(saved)}')
        return CreateOrganizationWalletsResult(wallets=saved, mnemonic=plaintext_mnemonic)

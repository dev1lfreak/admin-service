from __future__ import annotations

from src.application.abstractions import IUnitOfWork
from src.application.contracts import ILogger
from src.application.domain.entities.user import UserEntity, WalletEntity
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.crypto.wallet_crypto import (
    DerivedSecretKey,
    decrypt_mnemonic,
    derive_all_private_keys,
    is_crypto_ready,
)
from src.infrastructure.database.decorators import transactional


class ListUserWalletsCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, user_id: str) -> list[WalletEntity]:
        await self._unit_of_work.user_repository.get_by_id(user_id)
        return await self._unit_of_work.wallet_repository.list_by_user(user_id)


class GetUserMnemonicCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, user_id: str) -> str:
        user = await self._require_wallets_user(user_id)
        if not is_crypto_ready():
            raise ApplicationException(status_code=503, message='Crypto service not ready')
        return decrypt_mnemonic(user.encrypted_mnemonic or '')

    async def _require_wallets_user(self, user_id: str) -> UserEntity:
        user = await self._unit_of_work.user_repository.get_by_id(user_id)
        if not user.encrypted_mnemonic:
            raise ApplicationException(status_code=404, message='Wallets not created for user')
        return user


class GetUserSecretKeysCommand:
    def __init__(self, unit_of_work: IUnitOfWork, logger: ILogger):
        self._unit_of_work = unit_of_work
        self._logger = logger

    @transactional
    async def __call__(self, user_id: str) -> list[DerivedSecretKey]:
        user = await self._require_wallets_user(user_id)
        if not is_crypto_ready():
            raise ApplicationException(status_code=503, message='Crypto service not ready')
        mnemonic = decrypt_mnemonic(user.encrypted_mnemonic or '')
        return derive_all_private_keys(mnemonic)

    async def _require_wallets_user(self, user_id: str) -> UserEntity:
        user = await self._unit_of_work.user_repository.get_by_id(user_id)
        if not user.encrypted_mnemonic:
            raise ApplicationException(status_code=404, message='Wallets not created for user')
        return user
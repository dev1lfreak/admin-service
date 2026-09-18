from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.application.abstractions.repositories import (
    IAdminSessionRepository,
    IAdminUserRepository,
    ILegalEntityRepository,
    IOrganizationWalletRepository,
    IPurchaseRequestRepository,
    IUserRepository,
    IWalletRepository,
    IOrderRepository,
)


@runtime_checkable
class IUnitOfWork(Protocol):
    async def __aenter__(self) -> 'IUnitOfWork': ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...

    @property
    def user_repository(self) -> IUserRepository: ...

    @property
    def admin_user_repository(self) -> IAdminUserRepository: ...

    @property
    def admin_session_repository(self) -> IAdminSessionRepository: ...

    @property
    def legal_entity_repository(self) -> ILegalEntityRepository: ...

    @property
    def organization_wallet_repository(self) -> IOrganizationWalletRepository: ...

    @property
    def purchase_request_repository(self) -> IPurchaseRequestRepository: ...

    @property
    def wallet_repository(self) -> IWalletRepository: ...

    @property
    def order_repository(self) -> IOrderRepository: ...
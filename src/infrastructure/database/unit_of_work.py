from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.abstractions import IUnitOfWork
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
from src.application.contracts import ILogger
from src.application.domain.exceptions import RefreshConcurrentException
from src.infrastructure.database.repositories import (
    AdminSessionRepository,
    AdminUserRepository,
    LegalEntityRepository,
    OrganizationWalletRepository,
    PurchaseRequestRepository,
    UserRepository,
    WalletRepository,
    OrderRepository,
)


class UnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession], logger: ILogger):
        self.session_factory = session_factory
        self._session: AsyncSession | None = None
        self._user_repository: IUserRepository | None = None
        self._admin_user_repository: IAdminUserRepository | None = None
        self._admin_session_repository: IAdminSessionRepository | None = None
        self._legal_entity_repository: ILegalEntityRepository | None = None
        self._organization_wallet_repository: IOrganizationWalletRepository | None = None
        self._purchase_request_repository: IPurchaseRequestRepository | None = None
        self._wallet_repository: IWalletRepository | None = None
        self._order_repository: IOrderRepository | None = None
        self._logger: ILogger = logger

    async def __aenter__(self):
        self._session = self.session_factory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            if not isinstance(exc_val, RefreshConcurrentException):
                self._logger.error(str(exc_val))
            await self._session.rollback()
        else:
            await self._session.flush()
            await self._session.commit()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    @property
    def user_repository(self) -> IUserRepository:
        if self._user_repository is None:
            self._user_repository = UserRepository(session=self._session, logger=self._logger)
        return self._user_repository

    @property
    def admin_user_repository(self) -> IAdminUserRepository:
        if self._admin_user_repository is None:
            self._admin_user_repository = AdminUserRepository(session=self._session, logger=self._logger)
        return self._admin_user_repository

    @property
    def admin_session_repository(self) -> IAdminSessionRepository:
        if self._admin_session_repository is None:
            self._admin_session_repository = AdminSessionRepository(session=self._session, logger=self._logger)
        return self._admin_session_repository

    @property
    def legal_entity_repository(self) -> ILegalEntityRepository:
        if self._legal_entity_repository is None:
            self._legal_entity_repository = LegalEntityRepository(session=self._session, logger=self._logger)
        return self._legal_entity_repository

    @property
    def organization_wallet_repository(self) -> IOrganizationWalletRepository:
        if self._organization_wallet_repository is None:
            self._organization_wallet_repository = OrganizationWalletRepository(
                session=self._session, logger=self._logger
            )
        return self._organization_wallet_repository
    
    @property
    def wallet_repository(self) -> IWalletRepository:
        if self._wallet_repository is None:
            self._wallet_repository = WalletRepository(
                session=self._session, logger=self._logger
            )
        return self._wallet_repository

    @property
    def purchase_request_repository(self) -> IPurchaseRequestRepository:
        if self._purchase_request_repository is None:
            self._purchase_request_repository = PurchaseRequestRepository(
                session=self._session, logger=self._logger
            )
        return self._purchase_request_repository
    
    @property
    def order_repository(self) -> IOrderRepository:
        if self._order_repository is None:
            self._order_repository = OrderRepository(
                session=self._session, logger=self._logger
            )
        return self._order_repository

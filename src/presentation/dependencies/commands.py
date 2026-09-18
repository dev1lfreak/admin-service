from functools import lru_cache

from fastapi import Depends

from src.application.abstractions import IUnitOfWork
from src.application.commands import (
    AdminLoginCommand,
    AdminLogoutCommand,
    AdminJwtRefreshCommand,
    CreatePurchaseRequestCommand,
    GetAdminMeCommand,
    CreateOrganizationCommand,
    CreateOrganizationWalletsCommand,
    GetOrganizationMnemonicCommand,
    GetOrganizationSecretKeysCommand,
    GetOrganizationCommand,
    ListOrganizationWalletsCommand,
    GetPurchaseRequestCommand,
    ListOrganizationsCommand,
    GetOrganizationDocumentCommand,
    ListOrganizationDocumentsCommand,
    ListPurchaseRequestsCommand,
    SearchPartiesCommand,
    SetPurchaseRequestQuoteCommand,
    UpdateOrganizationCommand,
    UpdatePurchaseRequestCommand,
    UpdatePurchaseRequestStatusCommand,
    PutOrganizationDocumentCommand,
    SetPasswordCommand,
    ListUsersCommand,
    GetUserCommand,
    ListUserWalletsCommand,
    GetUserMnemonicCommand,
    GetUserSecretKeysCommand,
    ListOrdersCommand,
    ListUserOrdersCommand,
    ListOrdersByDateCommand,
    GetOrderCommand,
    GetPurchaseAnalyticsForYearCommand,
    GetOrdersAnalyticsForYearCommand,
    GetPurchaseAnalyticsForMonthCommand,
    GetOrdersAnalyticsForMonthCommand,
    GetPurchaseAnalyticsForWeekCommand,
    GetOrdersAnalyticsForWeekCommand,
)
from src.application.contracts import IHashService, IJwtService, ILogger
from src.infrastructure.config import settings
from src.infrastructure.storage.s3_documents_service import S3DocumentsService
from src.presentation.dependencies.logger import get_logger
from src.presentation.dependencies.security import get_hash_service, get_jwt_service
from src.presentation.dependencies.unit_of_work import get_unit_of_work


@lru_cache(maxsize=1)
def _s3_documents_service() -> S3DocumentsService:
    return S3DocumentsService(
        bucket=settings.LEGAL_DOCS_S3_BUCKET,
        region=settings.LEGAL_DOCS_S3_REGION,
        access_key_id=settings.LEGAL_DOCS_S3_ACCESS_KEY_ID or None,
        secret_access_key=settings.LEGAL_DOCS_S3_SECRET_ACCESS_KEY or None,
        endpoint_url=settings.LEGAL_DOCS_S3_ENDPOINT_URL or None,
        key_prefix=settings.LEGAL_DOCS_S3_KEY_PREFIX,
        presigned_ttl_seconds=settings.LEGAL_DOCS_S3_PRESIGNED_TTL_SECONDS,
    )


def get_s3_documents_service() -> S3DocumentsService:
    return _s3_documents_service()


def get_admin_login_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    hash_service: IHashService = Depends(get_hash_service),
    jwt_service: IJwtService = Depends(get_jwt_service),
    logger: ILogger = Depends(get_logger),
) -> AdminLoginCommand:
    return AdminLoginCommand(uow, hash_service, jwt_service, logger)


def get_admin_me_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetAdminMeCommand:
    return GetAdminMeCommand(uow, logger)


def get_admin_logout_command(
    logger: ILogger = Depends(get_logger),
) -> AdminLogoutCommand:
    return AdminLogoutCommand(logger)


def get_admin_jwt_refresh_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    jwt_service: IJwtService = Depends(get_jwt_service),
    logger: ILogger = Depends(get_logger),
) -> AdminJwtRefreshCommand:
    return AdminJwtRefreshCommand(uow, jwt_service, logger)


def get_create_organization_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    hash_service: IHashService = Depends(get_hash_service),
    logger: ILogger = Depends(get_logger),
) -> CreateOrganizationCommand:
    return CreateOrganizationCommand(uow, hash_service, logger)


def get_create_organization_wallets_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> CreateOrganizationWalletsCommand:
    return CreateOrganizationWalletsCommand(uow, logger)


def get_list_organization_wallets_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListOrganizationWalletsCommand:
    return ListOrganizationWalletsCommand(uow, logger)


def get_get_organization_mnemonic_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetOrganizationMnemonicCommand:
    return GetOrganizationMnemonicCommand(uow, logger)


def get_get_organization_secret_keys_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetOrganizationSecretKeysCommand:
    return GetOrganizationSecretKeysCommand(uow, logger)


def get_put_organization_document_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> PutOrganizationDocumentCommand:
    return PutOrganizationDocumentCommand(uow, get_s3_documents_service(), logger)


def get_list_organizations_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListOrganizationsCommand:
    return ListOrganizationsCommand(uow, logger)


def get_search_parties_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> SearchPartiesCommand:
    return SearchPartiesCommand(uow, logger)


def get_get_organization_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetOrganizationCommand:
    return GetOrganizationCommand(uow, logger)


def get_update_organization_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> UpdateOrganizationCommand:
    return UpdateOrganizationCommand(uow, logger)


def get_list_organization_documents_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListOrganizationDocumentsCommand:
    return ListOrganizationDocumentsCommand(uow, logger)


def get_get_organization_document_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetOrganizationDocumentCommand:
    return GetOrganizationDocumentCommand(uow, logger)


def get_list_purchase_requests_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListPurchaseRequestsCommand:
    return ListPurchaseRequestsCommand(uow, logger)


def get_create_purchase_request_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> CreatePurchaseRequestCommand:
    return CreatePurchaseRequestCommand(uow, logger)


def get_get_purchase_request_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetPurchaseRequestCommand:
    return GetPurchaseRequestCommand(uow, logger)


def get_update_purchase_request_status_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> UpdatePurchaseRequestStatusCommand:
    return UpdatePurchaseRequestStatusCommand(uow, logger)


def get_update_purchase_request_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> UpdatePurchaseRequestCommand:
    return UpdatePurchaseRequestCommand(uow, logger)


def get_set_purchase_request_quote_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> SetPurchaseRequestQuoteCommand:
    return SetPurchaseRequestQuoteCommand(uow, logger)

def get_set_password_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    hash_service: IHashService = Depends(get_hash_service),
    logger: ILogger = Depends(get_logger),
) -> SetPasswordCommand:
    return SetPasswordCommand(uow, hash_service, logger)

def get_list_users_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListUsersCommand:
    return ListUsersCommand(uow, logger)

def get_get_user_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetUserCommand:
    return GetUserCommand(uow, logger)

def get_list_user_wallets_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListUserWalletsCommand:
    return ListUserWalletsCommand(uow, logger)

def get_get_user_mnemonic_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetUserMnemonicCommand:
    return GetUserMnemonicCommand(uow, logger)

def get_get_user_secret_keys_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetUserSecretKeysCommand:
    return GetUserSecretKeysCommand(uow, logger)

def get_list_orders_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListOrdersCommand:
    return ListOrdersCommand(uow, logger)

def get_list_user_orders_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListUserOrdersCommand:
    return ListUserOrdersCommand(uow, logger)

def get_list_orders_by_date_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> ListOrdersByDateCommand:
    return ListOrdersByDateCommand(uow, logger)

def get_get_order_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetOrderCommand:
    return GetOrderCommand(uow, logger)

def get_get_purchase_analytics_for_year_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetPurchaseAnalyticsForYearCommand:
    return GetPurchaseAnalyticsForYearCommand(uow, logger)

def get_get_orders_analytics_for_year_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetOrdersAnalyticsForYearCommand:
    return GetOrdersAnalyticsForYearCommand(uow, logger)

def get_get_purchase_analytics_for_month_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetPurchaseAnalyticsForMonthCommand:
    return GetPurchaseAnalyticsForMonthCommand(uow, logger)

def get_get_orders_analytics_for_month_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetOrdersAnalyticsForMonthCommand:
    return GetOrdersAnalyticsForMonthCommand(uow, logger)

def get_get_purchase_analytics_for_week_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetPurchaseAnalyticsForWeekCommand:
    return GetPurchaseAnalyticsForWeekCommand(uow, logger)

def get_get_orders_analytics_for_week_command(
    uow: IUnitOfWork = Depends(get_unit_of_work),
    logger: ILogger = Depends(get_logger),
) -> GetOrdersAnalyticsForWeekCommand:
    return GetOrdersAnalyticsForWeekCommand(uow, logger)
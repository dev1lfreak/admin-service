from fastapi import APIRouter, Depends, Query, status

from src.application.commands import (
    CreateOrganizationCommand,
    CreateOrganizationWalletsCommand,
    GetOrganizationCommand,
    GetOrganizationMnemonicCommand,
    GetOrganizationSecretKeysCommand,
    ListOrganizationWalletsCommand,
    ListOrganizationsCommand,
    UpdateOrganizationCommand,
)
from src.application.domain.dto import AdminAuthContext
from src.presentation.decorators.admin_auth import require_admin_access, require_admin_role
from src.presentation.dependencies.commands import (
    get_create_organization_command,
    get_create_organization_wallets_command,
    get_get_organization_command,
    get_get_organization_mnemonic_command,
    get_get_organization_secret_keys_command,
    get_list_organization_wallets_command,
    get_list_organizations_command,
    get_update_organization_command,
)
from src.presentation.schemas.mappers import (
    create_wallets_to_response,
    mnemonic_to_response,
    organization_to_response,
    secret_key_to_response,
    wallet_to_response,
)
from src.presentation.schemas.organization import (
    CreateOrganizationRequest,
    OrganizationListResponse,
    OrganizationResponse,
    UpdateOrganizationRequest,
)
from src.presentation.schemas.entity import (
    CreateWalletsResponse,
    MnemonicResponse,
    SecretKeyResponse,
    WalletResponse,
)

organizations_router = APIRouter(prefix='/organizations', tags=['organizations'])


@organizations_router.get('', response_model=OrganizationListResponse)
async def list_organizations(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    q: str | None = Query(default=None, min_length=1, max_length=255),
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListOrganizationsCommand = Depends(get_list_organizations_command),
):
    items, total = await command(limit=limit, offset=offset, search=q)
    return OrganizationListResponse(
        items=[organization_to_response(x) for x in items],
        total=total,
    )


@organizations_router.post('', response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    body: CreateOrganizationRequest,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: CreateOrganizationCommand = Depends(get_create_organization_command),
):
    org = await command(
        admin_user_id=auth.admin_user_id,
        email=str(body.email),
        password=body.password,
        name=body.name,
        short_name=body.short_name,
        inn=body.inn,
        ogrn=body.ogrn,
        kpp=body.kpp,
        legal_address=body.legal_address,
        actual_address=body.actual_address,
        bank_details=body.bank_details,
        contact_person=body.contact_person,
        contact_phone=body.contact_phone,
        status=body.status,
    )
    return organization_to_response(org)


@organizations_router.get('/{organization_id}', response_model=OrganizationResponse)
async def get_organization(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetOrganizationCommand = Depends(get_get_organization_command),
):
    org = await command(organization_id)
    return organization_to_response(org)


@organizations_router.patch('/{organization_id}', response_model=OrganizationResponse)
async def update_organization(
    organization_id: str,
    body: UpdateOrganizationRequest,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: UpdateOrganizationCommand = Depends(get_update_organization_command),
):
    org = await command(organization_id, values=body.model_dump(exclude_unset=True))
    return organization_to_response(org)


@organizations_router.get('/{organization_id}/wallets', response_model=list[WalletResponse])
async def list_organization_wallets(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListOrganizationWalletsCommand = Depends(get_list_organization_wallets_command),
):
    wallets = await command(organization_id)
    return [wallet_to_response(w) for w in wallets]


@organizations_router.get('/{organization_id}/wallets/mnemonic', response_model=MnemonicResponse)
async def get_organization_mnemonic(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: GetOrganizationMnemonicCommand = Depends(get_get_organization_mnemonic_command),
):
    mnemonic = await command(organization_id)
    return mnemonic_to_response(mnemonic)


@organizations_router.get('/{organization_id}/wallets/secret-keys', response_model=list[SecretKeyResponse])
async def get_organization_secret_keys(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: GetOrganizationSecretKeysCommand = Depends(get_get_organization_secret_keys_command),
):
    keys = await command(organization_id)
    return [
        secret_key_to_response(
            chain=k.chain,
            address=k.address,
            derivation_path=k.derivation_path,
            private_key=k.private_key,
        )
        for k in keys
    ]


@organizations_router.post(
    '/{organization_id}/wallets/create',
    response_model=CreateWalletsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_organization_wallets(
    organization_id: str,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: CreateOrganizationWalletsCommand = Depends(get_create_organization_wallets_command),
):
    result = await command(organization_id=organization_id)
    return create_wallets_to_response(wallets=result.wallets, mnemonic=result.mnemonic)

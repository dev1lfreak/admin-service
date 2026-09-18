from fastapi import APIRouter, Depends, Request, Query, status
from fastapi.responses import ORJSONResponse
from starlette import status

from src.application.domain.dto import AdminAuthContext
from src.presentation.decorators.admin_auth import require_admin_access, require_admin_role
from src.presentation.dependencies.commands import (
    get_set_password_command,
    get_list_users_command,
    get_get_user_command,
    get_list_user_wallets_command,
    get_get_user_mnemonic_command,
    get_get_user_secret_keys_command,
    get_list_user_orders_command,
)
from src.presentation.schemas.mappers import (
    mnemonic_to_response,
    user_to_response,
    secret_key_to_response,
    wallet_to_response,
    order_to_response,
)
from src.presentation.schemas.user import (
    UserResponse,
    UserListResponse,
)
from src.presentation.schemas.entity import (
    MnemonicResponse,
    SecretKeyResponse,
    WalletResponse,
)
from src.presentation.schemas.order import (
    OrdersResponse,
)
from src.application.commands.set_password import SetPasswordCommand
from src.application.commands.user_commands import (
    ListUsersCommand,
    GetUserCommand,
)
from src.application.commands.user_wallet_commands import (
    ListUserWalletsCommand,
    GetUserMnemonicCommand,
    GetUserSecretKeysCommand
)
from src.application.commands.orders_commands import (
    ListUserOrdersCommand,
)
from src.presentation.schemas.password import SetPasswordRequest


users_router = APIRouter(prefix='/users', tags=['users'])

@users_router.get('', response_model=UserListResponse)
async def list_users(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    q: str | None = Query(default=None, min_length=1, max_length=255),
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListUsersCommand = Depends(get_list_users_command),
):
    items, total = await command(limit=limit, offset=offset, search=q)
    return UserListResponse(
        items=[user_to_response(x) for x in items],
        total=total,
    )

@users_router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetUserCommand = Depends(get_get_user_command),
):
    user = await command(user_id)
    return user_to_response(user)

@users_router.get('/{user_id}/wallets', response_model=list[WalletResponse])
async def list_user_wallets(
    user_id: str,
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListUserWalletsCommand = Depends(get_list_user_wallets_command),
):
    wallets = await command(user_id)
    return [wallet_to_response(w) for w in wallets]


@users_router.get('/{user_id}/orders', response_model=OrdersResponse)
async def list_user_orders(
    user_id: str,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    auth: AdminAuthContext = Depends(require_admin_access),
    command: ListUserOrdersCommand = Depends(get_list_user_orders_command),
):
    orders, total = await command(user_id=user_id, limit=limit, offset=offset)
    return OrdersResponse(
        items=[order_to_response(o) for o in orders],
        total=total,
    )


@users_router.get('/{user_id}/wallets/mnemonic', response_model=MnemonicResponse)
async def get_user_mnemonic(
    user_id: str,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: GetUserMnemonicCommand = Depends(get_get_user_mnemonic_command),
):
    mnemonic = await command(user_id)
    return mnemonic_to_response(mnemonic)


@users_router.get('/{user_id}/wallets/secret-keys', response_model=list[SecretKeyResponse])
async def get_user_secret_keys(
    user_id: str,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: GetUserSecretKeysCommand = Depends(get_get_user_secret_keys_command),
):
    keys = await command(user_id)
    return [
        secret_key_to_response(
            chain=k.chain,
            address=k.address,
            derivation_path=k.derivation_path,
            private_key=k.private_key,
        )
        for k in keys
    ]


@users_router.patch(path='/change_password', response_class=ORJSONResponse, status_code=status.HTTP_200_OK)
async def change_password(
    request: Request, 
    body: SetPasswordRequest,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: SetPasswordCommand = Depends(get_set_password_command),
):
    await command(email=body.email, password=body.password)
    return ORJSONResponse(content={'message': 'Password updated successfully'})


@users_router.patch(path='/{user_id}/set_password', response_class=ORJSONResponse, status_code=status.HTTP_200_OK)
async def set_password(
    user_id: str,
    request: Request, 
    body: SetPasswordRequest,
    auth: AdminAuthContext = Depends(require_admin_role('compliance', 'superadmin')),
    command: SetPasswordCommand = Depends(get_set_password_command),
):
    await command(user_id=user_id, password=body.password)
    return ORJSONResponse(content={'message': 'Password updated successfully'})

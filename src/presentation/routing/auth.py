from fastapi import APIRouter, Depends, status
from fastapi.responses import ORJSONResponse

from src.application.commands import AdminJwtRefreshCommand, AdminLoginCommand, GetAdminMeCommand
from src.application.domain.dto import AdminAuthContext
from src.presentation.auth_cookies import set_auth_cookies
from src.presentation.decorators.admin_auth import require_admin_access
from src.presentation.dependencies.commands import (
    get_admin_jwt_refresh_command,
    get_admin_login_command,
    get_admin_me_command,
)
from src.presentation.schemas.admin_auth import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminMeResponse,
    AdminRefreshRequest,
    AdminRefreshResponse,
)

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post('/login', response_model=AdminLoginResponse, status_code=status.HTTP_200_OK)
async def admin_login(
    body: AdminLoginRequest,
    command: AdminLoginCommand = Depends(get_admin_login_command),
):
    dto = await command(login=body.login, password=body.password)
    response = ORJSONResponse(
        AdminLoginResponse(
            access_token=dto.access_token,
            refresh_token=dto.refresh_token,
            id=dto.id,
            login=dto.login,
            first_name=dto.first_name,
            last_name=dto.last_name,
            role=dto.role,
        ).model_dump()
    )
    set_auth_cookies(response, dto.access_token, dto.refresh_token)
    return response


@auth_router.post('/refresh', response_model=AdminRefreshResponse, status_code=status.HTTP_200_OK)
async def admin_refresh(
    body: AdminRefreshRequest,
    command: AdminJwtRefreshCommand = Depends(get_admin_jwt_refresh_command),
):
    access, refresh = await command(refresh_token=body.refresh_token)
    return AdminRefreshResponse(access_token=access, refresh_token=refresh)


@auth_router.post('/logout', response_class=ORJSONResponse, status_code=status.HTTP_200_OK)
async def admin_logout():
    return {'ok': True}


@auth_router.get('/me', response_model=AdminMeResponse)
async def admin_me(
    auth: AdminAuthContext = Depends(require_admin_access),
    command: GetAdminMeCommand = Depends(get_admin_me_command),
):
    admin = await command(auth.admin_user_id)
    return AdminMeResponse(
        id=admin.id,
        login=admin.login,
        first_name=admin.first_name,
        last_name=admin.last_name,
        role=admin.role,
    )

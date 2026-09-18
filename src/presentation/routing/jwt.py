from fastapi import APIRouter, Depends, Request
from fastapi.responses import ORJSONResponse
from starlette import status

from src.application.commands import AdminJwtRefreshCommand
from src.application.domain.exceptions import ApplicationException
from src.presentation.auth_cookies import clear_auth_cookies, set_auth_cookies
from src.presentation.dependencies.commands import get_admin_jwt_refresh_command

jwt_router = APIRouter(prefix='/jwt', tags=['jwt'])


@jwt_router.post('/refresh', response_class=ORJSONResponse, status_code=status.HTTP_200_OK)
async def refresh_tokens(
    request: Request,
    command: AdminJwtRefreshCommand = Depends(get_admin_jwt_refresh_command),
):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        response = ORJSONResponse({'result': False, 'error': 'No refresh token'}, status_code=401)
        clear_auth_cookies(response)
        return response

    try:
        access, refresh = await command(refresh_token=refresh_token)
    except ApplicationException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            response = ORJSONResponse({'result': False}, status_code=401)
            clear_auth_cookies(response)
            return response
        raise

    response = ORJSONResponse({'result': True})
    set_auth_cookies(response, access, refresh)
    return response

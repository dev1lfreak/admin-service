from fastapi import Depends, Request
from fastapi.security.utils import get_authorization_scheme_param

from src.application.contracts import IJwtService
from src.application.domain.dto import AdminAuthContext
from src.application.domain.exceptions import ApplicationException
from src.presentation.dependencies.security import get_jwt_service


def _extract_bearer_token(request: Request) -> str | None:
    auth = request.headers.get('Authorization')
    if not auth:
        return None
    scheme, param = get_authorization_scheme_param(auth)
    if scheme.lower() == 'bearer' and param:
        return param
    return None


async def require_admin_access(
    request: Request,
    jwt_service: IJwtService = Depends(get_jwt_service),
) -> AdminAuthContext:
    token = _extract_bearer_token(request)
    if not token:
        raise ApplicationException(status_code=401, message='Authorization Bearer token required')

    payload = await jwt_service.decode_access_token(token)
    if payload.type != 'access':
        raise ApplicationException(status_code=401, message='Invalid token type')

    role = payload.role
    if not role:
        raise ApplicationException(status_code=401, message='Token missing role')

    return AdminAuthContext(admin_user_id=payload.sub, role=role)


def require_admin_role(*allowed_roles: str):
    allowed = set(allowed_roles)

    async def dependency(auth: AdminAuthContext = Depends(require_admin_access)) -> AdminAuthContext:
        if auth.role not in allowed:
            raise ApplicationException(status_code=403, message='Insufficient permissions')
        return auth

    return dependency

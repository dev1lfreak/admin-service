from fastapi.responses import ORJSONResponse

from src.infrastructure.config import settings


def clear_auth_cookies(response: ORJSONResponse) -> None:
    response.delete_cookie('access_token', path='/', domain=settings.ADMIN_COOKIE_DOMAIN)
    response.delete_cookie('refresh_token', path='/', domain=settings.ADMIN_COOKIE_DOMAIN)


def set_auth_cookies(response: ORJSONResponse, access: str, refresh: str) -> None:
    response.set_cookie(
        key='access_token',
        value=access,
        httponly=True,
        secure=settings.ADMIN_COOKIE_SECURE,
        samesite='lax',
        path='/',
        domain=settings.ADMIN_COOKIE_DOMAIN,
        max_age=int(settings.JWT_ACCESS_TTL_SECONDS),
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh,
        httponly=True,
        secure=settings.ADMIN_COOKIE_SECURE,
        samesite='lax',
        path='/',
        domain=settings.ADMIN_COOKIE_DOMAIN,
        max_age=int(settings.JWT_REFRESH_TTL_SECONDS),
    )

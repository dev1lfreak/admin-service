from fastapi import Request
from fastapi.responses import ORJSONResponse
from src.application.domain.exceptions import ApplicationException


async def application_exception_handler(_request: Request, exc: ApplicationException) -> ORJSONResponse:
    detail = exc.message
    if 500 <= exc.status_code:
        detail = 'Internal Server Error'

    return ORJSONResponse(
        status_code=exc.status_code,
        content={'detail': detail},
        headers=dict(exc.headers) if exc.headers else None,
    )

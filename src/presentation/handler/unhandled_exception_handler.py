from fastapi import Request
from fastapi.responses import ORJSONResponse
from starlette import status
from src.infrastructure.logger import logger


async def unhandled_exception_handler(_request: Request, exc: Exception) -> ORJSONResponse:
    logger.exception(f'Unhandled exception: {type(exc).__name__}')
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': 'Internal Server Error'},
    )

from typing import Mapping
from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class UnauthorizedException(ApplicationException):
    def __init__(
        self,
        message: str = 'Unauthorized',
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            headers=headers,
        )

from typing import Mapping
from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class TooManyRequestsException(ApplicationException):
    def __init__(
        self,
        message: str = 'Too Many Requests',
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            message=message,
            headers=headers,
        )

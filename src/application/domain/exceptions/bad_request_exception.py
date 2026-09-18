from typing import Mapping
from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class BadRequestException(ApplicationException):
    def __init__(
        self,
        message: str = 'Bad Request',
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            headers=headers,
        )

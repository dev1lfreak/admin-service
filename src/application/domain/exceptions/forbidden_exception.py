from typing import Mapping
from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class ForbiddenException(ApplicationException):
    def __init__(
        self,
        message: str = 'Forbidden',
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            headers=headers,
        )

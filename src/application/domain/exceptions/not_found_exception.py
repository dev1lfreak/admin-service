from typing import Mapping
from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class NotFoundException(ApplicationException):
    def __init__(
        self,
        message: str = 'Not Found',
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            headers=headers,
        )

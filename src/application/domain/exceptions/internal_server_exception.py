from typing import Mapping
from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class InternalServerException(ApplicationException):
    def __init__(
        self,
        message: str = 'Internal Server Error',
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            headers=headers,
        )

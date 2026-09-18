from typing import Mapping
from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class ServiceUnavailableException(ApplicationException):
    def __init__(
        self,
        message: str = 'Service Unavailable',
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=message,
            headers=headers,
        )

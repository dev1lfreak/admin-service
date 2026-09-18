from typing import Mapping
from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class ConflictException(ApplicationException):
    def __init__(
        self,
        message: str = 'Conflict',
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            headers=headers,
        )

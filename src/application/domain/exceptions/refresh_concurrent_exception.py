from starlette import status
from src.application.domain.exceptions.application_exception import ApplicationException


class RefreshConcurrentException(ApplicationException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_200_OK,
            message='Refresh already handled',
        )

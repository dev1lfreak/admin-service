from __future__ import annotations
from typing import Mapping


class ApplicationException(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        headers: Mapping[str, str] | None = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        self.headers = headers

    def __str__(self):
        return f'{self.status_code}: {self.message}'

from __future__ import annotations

from src.application.contracts import ILogger


class AdminLogoutCommand:
    def __init__(self, logger: ILogger):
        self._logger = logger

    async def __call__(self) -> None:
        self._logger.debug('Admin logout (stateless)')

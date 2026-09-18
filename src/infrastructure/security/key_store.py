from __future__ import annotations

from datetime import datetime, timezone

from src.application.domain.dto import JwtKeyPair, JwtKeySet
from src.application.domain.exceptions import ApplicationException


class JwtKeyStore:
    _instance: JwtKeyStore | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        *,
        active_kid: str,
        private_key: str,
        public_key: str,
        previous_kid: str | None = None,
        previous_public_key: str | None = None,
    ) -> None:
        if getattr(self, '_initialized', False):
            return
        previous = None
        if previous_kid and previous_public_key:
            previous = JwtKeyPair(
                kid=previous_kid,
                private_key_pem='',
                public_key_pem=previous_public_key,
            )
        self._keyset = JwtKeySet(
            active=JwtKeyPair(kid=active_kid, private_key_pem=private_key, public_key_pem=public_key),
            previous=previous,
        )
        self._last_refresh_at = datetime.now(timezone.utc)
        self._initialized = True

    @classmethod
    def get_instance(cls) -> JwtKeyStore:
        if cls._instance is None:
            raise ApplicationException(status_code=500, message='JwtKeyStore not initialized')
        return cls._instance

    async def get_signing_key(self) -> tuple[str, str]:
        return self._keyset.active.kid, self._keyset.active.private_key_pem

    async def get_public_key_for_kid(self, kid: str) -> str | None:
        return self._keyset.public_keys_by_kid().get(kid)

    async def last_refresh_at(self) -> datetime | None:
        return self._last_refresh_at

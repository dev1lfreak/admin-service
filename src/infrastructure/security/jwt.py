from __future__ import annotations

from datetime import datetime, timezone, timedelta

from jose import jwt, ExpiredSignatureError, JWTError

from src.application.contracts import ILogger, IJwtService
from src.application.domain.dto import AccessTokenPayload, RefreshTokenPayload
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.config.settings import settings
from src.infrastructure.security.key_store import JwtKeyStore


class JwtService(IJwtService):
    def __init__(self, logger: ILogger, key_store: JwtKeyStore) -> None:
        self._logger = logger
        self._key_store = key_store

    @property
    def _issuer(self) -> str | None:
        return settings.ADMIN_JWT_ISSUER

    async def create_access_token(self, user_id: str, *, role: str) -> str:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(seconds=int(settings.JWT_ACCESS_TTL_SECONDS))

        payload: dict[str, object] = {
            'sub': user_id,
            'type': 'access',
            'role': role,
            'iat': int(now.timestamp()),
            'nbf': int(now.timestamp()),
            'exp': int(exp.timestamp()),
        }
        if self._issuer:
            payload['iss'] = self._issuer
        if settings.JWT_AUDIENCE:
            payload['aud'] = settings.JWT_AUDIENCE

        return await self._encode(payload, user_id=user_id, token_kind='access')

    async def create_refresh_token(self, user_id: str, *, role: str) -> str:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(seconds=int(settings.JWT_REFRESH_TTL_SECONDS))

        payload: dict[str, object] = {
            'sub': user_id,
            'type': 'refresh',
            'role': role,
            'iat': int(now.timestamp()),
            'nbf': int(now.timestamp()),
            'exp': int(exp.timestamp()),
        }
        if self._issuer:
            payload['iss'] = self._issuer
        if settings.JWT_AUDIENCE:
            payload['aud'] = settings.JWT_AUDIENCE

        return await self._encode(payload, user_id=user_id, token_kind='refresh')

    async def _encode(self, payload: dict[str, object], *, user_id: str, token_kind: str) -> str:
        try:
            kid, private_pem = await self._key_store.get_signing_key()
            token = jwt.encode(payload, private_pem, algorithm=settings.JWT_ALGORITHM, headers={'kid': kid})
            self._logger.info(f'Admin {token_kind} token created admin_user_id={user_id} kid={kid}')
            return token
        except ApplicationException:
            raise
        except Exception as exception:
            self._logger.error(f'JWT signing failed admin_user_id={user_id} error={exception}')
            raise ApplicationException(status_code=500, message='JWT signing failed')

    async def decode_access_token(self, token: str) -> AccessTokenPayload:
        payload = await self._decode_and_verify(token)
        if payload.get('type') != 'access':
            raise ApplicationException(status_code=401, message='Invalid token type')
        try:
            return AccessTokenPayload(
                sub=str(payload['sub']),
                type='access',
                role=str(payload['role']) if payload.get('role') else None,
                iat=int(payload['iat']),
                nbf=int(payload['nbf']),
                exp=int(payload['exp']),
                iss=payload.get('iss'),
                aud=payload.get('aud'),
            )
        except KeyError as exception:
            raise ApplicationException(status_code=401, message=f'Missing token claim: {exception}')

    async def decode_refresh_token(self, token: str) -> RefreshTokenPayload:
        payload = await self._decode_and_verify(token)
        if payload.get('type') != 'refresh':
            raise ApplicationException(status_code=401, message='Invalid token type')
        try:
            return RefreshTokenPayload(
                sub=str(payload['sub']),
                type='refresh',
                role=str(payload['role']),
                iat=int(payload['iat']),
                nbf=int(payload['nbf']),
                exp=int(payload['exp']),
                iss=payload.get('iss'),
                aud=payload.get('aud'),
            )
        except KeyError as exception:
            raise ApplicationException(status_code=401, message=f'Missing token claim: {exception}')

    async def _decode_and_verify(self, token: str) -> dict:
        kid: str | None = None
        try:
            header = jwt.get_unverified_header(token)
            kid = header.get('kid')
            if not kid:
                raise ApplicationException(status_code=401, message='Missing token header: kid')
            if header.get('alg') != settings.JWT_ALGORITHM:
                raise ApplicationException(status_code=401, message='Invalid token algorithm')

            public_pem = await self._key_store.get_public_key_for_kid(str(kid))
            if not public_pem:
                raise ApplicationException(status_code=401, message='Unknown token kid')

            options = {
                'verify_signature': True,
                'verify_exp': True,
                'verify_nbf': True,
                'verify_iat': True,
                'verify_aud': bool(settings.JWT_AUDIENCE),
                'verify_iss': bool(self._issuer),
                'require_exp': True,
                'require_iat': True,
                'require_nbf': True,
                'require_sub': True,
                'leeway': 10,
            }

            payload = jwt.decode(
                token,
                public_pem,
                algorithms=[settings.JWT_ALGORITHM],
                audience=settings.JWT_AUDIENCE or None,
                issuer=self._issuer or None,
                options=options,
            )
            if 'type' not in payload:
                raise ApplicationException(status_code=401, message='Missing token claim: type')
            token_type = payload.get('type')
            if 'role' not in payload:
                raise ApplicationException(status_code=401, message='Missing token claim: role')
            if token_type not in ('access', 'refresh'):
                raise ApplicationException(status_code=401, message='Invalid token type')
            return payload
        except ExpiredSignatureError:
            raise ApplicationException(status_code=401, message='Token expired')
        except ApplicationException:
            raise
        except JWTError:
            raise ApplicationException(status_code=401, message='Invalid token')
        except Exception as exception:
            self._logger.error(f'Unexpected JWT decode error kid={kid} error={exception}')
            raise ApplicationException(status_code=500, message='JWT decode failed')

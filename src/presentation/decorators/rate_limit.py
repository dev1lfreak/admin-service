from __future__ import annotations
import functools
import inspect
import hashlib
from typing import Any, Awaitable, Callable, Literal, Optional, Protocol, runtime_checkable
from fastapi import Request
from redis.asyncio.client import Redis
from src.application.contracts import ILogger
from src.application.domain.exceptions import ApplicationException
from src.infrastructure.logger import get_logger
from src.presentation.dependencies import get_redis


def _find_request(args: tuple[Any, ...], kwargs: dict[str, Any]) -> Request:
    req = kwargs.get('request')
    if isinstance(req, Request):
        return req
    for a in args:
        if isinstance(a, Request):
            return a
    raise RuntimeError('rate_limit decorator requires fastapi.Request argument')


def _client_ip(request: Request) -> str:
    xff = request.headers.get('x-forwarded-for')
    if xff:
        return xff.split(',')[0].strip()
    if request.client:
        return request.client.host
    return 'unknown'


_LUA_INCR_EXPIRE_TTL = '''
local key = KEYS[1]
local window = tonumber(ARGV[1])

local current = redis.call('INCR', key)
if current == 1 then
  redis.call('EXPIRE', key, window)
end

local ttl = redis.call('TTL', key)
return { current, ttl }
'''


Scope = Literal['ip', 'device', 'user', 'key']


@runtime_checkable
class KeyBuilder1(Protocol):
    def __call__(self, request: Request) -> str: ...


@runtime_checkable
class KeyBuilder3(Protocol):
    def __call__(self, request: Request, args: tuple[Any, ...], kwargs: dict[str, Any]) -> str: ...


KeyBuilder = KeyBuilder1 | KeyBuilder3


def _call_key_builder(builder: KeyBuilder, request: Request, args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:
    try:
        sig = inspect.signature(builder)
        if len(sig.parameters) >= 3:
            return builder(request, args, kwargs)
        return builder(request)
    except Exception as e:
        try:
            return builder(request, args, kwargs)
        except Exception:
            raise e
        
def _email_rl_key(request: Request, args: tuple[Any, ...], kwargs: dict[str, Any]) -> str:

    body = kwargs.get('body')
    if body is None and args:
        for a in args:
            if hasattr(a, 'email'):
                body = a
                break

    email = (getattr(body, 'email', '') or '').strip().lower()
    if not email:
        email = _client_ip(request)

    digest = hashlib.sha256(email.encode('utf-8')).hexdigest()[:24]
    return f'email:{digest}'

def rate_limit(
    *,
    limit: int,
    window_seconds: int,
    scope: Scope = 'ip',
    key_prefix: str = 'rl',
    key_builder: Optional[KeyBuilder] = None,
    fail_open: bool = True,
) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:

    if limit <= 0:
        raise ValueError('rate_limit: limit must be > 0')
    if window_seconds <= 0:
        raise ValueError('rate_limit: window_seconds must be > 0')
    if scope == 'key' and not key_builder:
        raise ValueError('rate_limit: scope="key" requires key_builder')

    def decorator(func: Callable[..., Awaitable[Any]]):
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            request = _find_request(args, kwargs)
            logger: ILogger = get_logger()

            if scope == 'ip':
                ident = _client_ip(request)
            elif scope == 'device':
                ident = request.cookies.get('device_id') or _client_ip(request)
            elif scope == 'user':
                user = getattr(request.state, 'user', None)
                user_id = getattr(user, 'id', None) if user else None
                ident = str(user_id) if user_id else _client_ip(request)
            else:
                try:
                    ident = _call_key_builder(key_builder, request, args, kwargs)  # type: ignore[arg-type]
                except Exception as e:
                    logger.error(f'RateLimit key_builder failed error={str(e)}')
                    raise ApplicationException(500, 'Rate limiter key_builder failed')

            route = request.url.path
            method = request.method
            redis_key = f'{key_prefix}:{scope}:{method}:{route}:{ident}'

            logger.debug(f'RateLimit check key={redis_key} limit={limit} window={window_seconds}')

            try:
                redis: Redis = get_redis(request)

                result = await redis.eval(
                    _LUA_INCR_EXPIRE_TTL,
                    1,
                    redis_key,
                    str(window_seconds),
                )

                count = int(result[0])
                ttl_raw = int(result[1]) if result and len(result) > 1 else window_seconds
                ttl = window_seconds if ttl_raw < 0 else ttl_raw

            except Exception as e:
                logger.error(f'RateLimit redis failure key={redis_key} error={str(e)}')

                if fail_open:
                    logger.warning(f'RateLimit fail-open activated key={redis_key}')
                    return await func(*args, **kwargs)

                raise ApplicationException(503, 'Rate limiter unavailable')

            if count > limit:
                retry_after = max(ttl, 0)
                logger.warning(f'RateLimit exceeded key={redis_key} count={count} limit={limit} retry_after={retry_after}')
                raise ApplicationException(
                    status_code=429,
                    message='Too Many Requests',
                    headers={'Retry-After': str(retry_after)},
                )

            logger.debug(f'RateLimit passed key={redis_key} count={count}')
            return await func(*args, **kwargs)

        return wrapper
    return decorator
from functools import lru_cache
from fastapi import Depends
from src.application.contracts import IHashService, IJwtService, ILogger
from src.infrastructure.security import HashService, JwtService
from src.infrastructure.security.key_store import JwtKeyStore
from src.presentation.dependencies.logger import get_logger


@lru_cache(maxsize=1)
def _hash_service(logger: ILogger) -> IHashService:
    return HashService(logger=logger)


def get_hash_service(logger: ILogger = Depends(get_logger)) -> IHashService:
    return _hash_service(logger)


@lru_cache(maxsize=1)
def _jwt_service(logger: ILogger) -> IJwtService:
    key_store = JwtKeyStore.get_instance()
    return JwtService(logger=logger, key_store=key_store)


def get_jwt_service(logger: ILogger = Depends(get_logger)) -> IJwtService:
    return _jwt_service(logger)
from __future__ import annotations

from functools import lru_cache
from typing import List, Literal
from dotenv import load_dotenv, find_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = find_dotenv(".env")
if env_file:
    load_dotenv(env_file)


class Settings(BaseSettings):
    JWT_ACTIVE_KID: str
    JWT_PRIVATE_KEY: str
    JWT_PUBLIC_KEY: str
    JWT_PREVIOUS_KID: str | None = None
    JWT_PREVIOUS_PUBLIC_KEY: str | None = None
    CRYPTO_MASTER_KEY: str

    DATABASE_HOST: str
    DATABASE_PORT: int = Field(default=5432, ge=1, le=65535)
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600
    DATABASE_ECHO: bool = False

    ADMIN_COOKIE_SECURE: bool = False
    ADMIN_COOKIE_DOMAIN: str | None = '.elcsa.ru'
    CORS_ALLOW_ORIGIN_REGEX: str = r'https?://([a-z0-9-]+\.)*elcsa\.ru(:\d+)?$'

    DOCS_USERNAME: str = 'admin'
    DOCS_PASSWORD: str = 'admin'

    JWT_ACCESS_TTL_SECONDS: int = 8 * 60 * 60
    JWT_REFRESH_TTL_SECONDS: int = 30 * 24 * 60 * 60
    ADMIN_JWT_ISSUER: str | None = 'admin-service'
    JWT_AUDIENCE: str | None = None
    JWT_ALGORITHM: str = 'RS256'

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str | None = None
    REDIS_DB: int = 0

    LEGAL_DOCS_S3_BUCKET: str = ''
    LEGAL_DOCS_S3_REGION: str = 'us-east-1'
    LEGAL_DOCS_S3_ACCESS_KEY_ID: str = ''
    LEGAL_DOCS_S3_SECRET_ACCESS_KEY: str = ''
    LEGAL_DOCS_S3_ENDPOINT_URL: str = ''
    LEGAL_DOCS_S3_KEY_PREFIX: str = 'legal-docs'
    LEGAL_DOCS_S3_PRESIGNED_TTL_SECONDS: int = 3600

    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_WINDOW: int = 60

    LOG_LEVEL: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = 'INFO'
    LOG_FORMAT: Literal['JSON', 'TEXT'] = 'JSON'

    @field_validator('ADMIN_COOKIE_DOMAIN', mode='before')
    @classmethod
    def normalize_admin_cookie_domain(cls, v):
        if v is None or (isinstance(v, str) and not v.strip()):
            return '.elcsa.ru'
        s = str(v).strip()
        sl = s.lower()
        if sl in ('.elcsa.ru', 'elcsa.ru'):
            return '.elcsa.ru'
        if sl.endswith('.elcsa.ru') and not sl.startswith('.'):
            return '.elcsa.ru'
        return s

    @field_validator('REDIS_PASSWORD', mode='before')
    @classmethod
    def empty_redis_password_to_none(cls, v):
        if v is None or (isinstance(v, str) and not v.strip()):
            return None
        return v

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore',
        populate_by_name=True,
    )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def REDIS_URL(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}'

    @property
    def EXCLUDED_PATHS(self) -> List[str]:
        return ['/docs', '/redoc', '/openapi.json', '/ping', '/health']


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

from dataclasses import dataclass
from datetime import datetime, date


@dataclass(slots=True)
class UserCreatedDto:
    id: str
    email: str
    access_token: str
    refresh_token: str


@dataclass(slots=True)
class UserLoginDto:
    id: str | None = None
    email: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    birth_date: date | None = None
    encrypted_mnemonic: str | None = None
    phone: str | None = None
    passport_data: str | None = None
    inn: str | None = None
    erc20: str | None = None
    avatar_link: str | None = None
    kyc_verified: bool | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    kyc_verified_at: datetime | None = None


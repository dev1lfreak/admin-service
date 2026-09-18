from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime


@dataclass(slots=True)
class UserEntity:
    id: str | None = None
    email: str | None = None
    password_hash: str | None = None

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
    is_deleted: bool | None = None

    created_at: datetime | None = None
    updated_at: datetime | None = None
    kyc_verified_at: datetime | None = None
    account_type: str | None = None
    provisioned_by: str | None = None
    provisioned_at: datetime | None = None

@dataclass
class WalletEntity:
    id: str
    user_id: str
    chain: str
    address: str
    derivation_path: str
    created_at: datetime | None = None

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any


@dataclass
class LegalEntityEntity:
    id: str
    user_id: str
    name: str
    short_name: str | None
    inn: str
    ogrn: str | None
    kpp: str | None
    legal_address: str | None
    actual_address: str | None
    bank_details: dict[str, Any] | None
    contact_person: str | None
    contact_phone: str | None
    status: str
    kyc_verified: bool
    kyc_verified_at: datetime | None
    encrypted_mnemonic: str | None
    document_s3_keys: dict[str, str | None]
    created_by: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass
class OrganizationWalletEntity:
    id: str
    organization_id: str
    chain: str
    address: str
    derivation_path: str
    created_at: datetime | None = None


@dataclass
class CreateOrganizationWalletsResult:
    wallets: list[OrganizationWalletEntity]
    mnemonic: str


@dataclass
class OrganizationDocumentSlot:
    organization_id: str
    document_type: str
    s3_key: str | None
    file_name: str | None = None
    content_type: str | None = None
    file_size_bytes: int | None = None


@dataclass
class PurchaseRequestEntity:
    id: str
    organization_id: str
    status: str
    rub_amount: Decimal
    usdt_amount: Decimal | None
    exchange_rate: Decimal | None
    service_fee_percent: Decimal | None
    comment: str | None
    admin_comment: str | None
    target_wallet_chain: str | None
    target_wallet_address: str | None
    tx_hash: str | None
    assigned_to: str | None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    completed_at: datetime | None = None

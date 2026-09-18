from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field


class PartySearchResponse(BaseModel):
    id: str
    account_type: str
    user_id: str
    email: str | None
    name: str | None
    inn: str | None
    phone: str | None
    status: str | None
    kyc_verified: bool | None
    created_at: str | None


class PartySearchListResponse(BaseModel):
    items: list[PartySearchResponse]
    total: int


class WalletResponse(BaseModel):
    id: str
    chain: str
    address: str
    derivation_path: str
    created_at: str | None


class CreateWalletsResponse(BaseModel):
    wallets: list[WalletResponse]
    mnemonic: str


class MnemonicResponse(BaseModel):
    mnemonic: str


class SecretKeyResponse(BaseModel):
    chain: str
    address: str
    derivation_path: str
    private_key: str


class CreatePurchaseRequestBody(BaseModel):
    organization_id: str
    rub_amount: Decimal = Field(gt=0)
    status: str = 'submitted'
    usdt_amount: Decimal | None = Field(default=None, gt=0)
    exchange_rate: Decimal | None = Field(default=None, gt=0)
    service_fee_percent: Decimal | None = Field(default=None, ge=0)
    comment: str | None = None
    admin_comment: str | None = None
    target_wallet_chain: str | None = Field(default='ETH', max_length=16)
    target_wallet_address: str | None = Field(default=None, max_length=128)
    tx_hash: str | None = Field(default=None, max_length=128)
    assigned_to: str | None = None


class UpdatePurchaseRequestStatusBody(BaseModel):
    status: str
    admin_comment: str | None = None
    assigned_to: str | None = None
    tx_hash: str | None = None


class UpdatePurchaseRequestBody(BaseModel):
    status: str | None = None
    rub_amount: Decimal | None = Field(default=None, gt=0)
    usdt_amount: Decimal | None = Field(default=None, gt=0)
    exchange_rate: Decimal | None = Field(default=None, gt=0)
    service_fee_percent: Decimal | None = Field(default=None, ge=0)
    comment: str | None = None
    admin_comment: str | None = None
    target_wallet_chain: str | None = Field(default=None, max_length=16)
    target_wallet_address: str | None = Field(default=None, max_length=128)
    tx_hash: str | None = Field(default=None, max_length=128)
    assigned_to: str | None = None


class SetPurchaseRequestQuoteBody(BaseModel):
    rub_amount: Decimal = Field(gt=0)
    exchange_rate: Decimal = Field(gt=0)
    service_fee_percent: Decimal | None = None
    admin_comment: str | None = None


class PurchaseRequestResponse(BaseModel):
    id: str
    organization_id: str
    status: str
    rub_amount: str
    usdt_amount: str | None
    exchange_rate: str | None
    service_fee_percent: str | None
    comment: str | None
    admin_comment: str | None
    target_wallet_chain: str | None
    target_wallet_address: str | None
    tx_hash: str | None
    assigned_to: str | None
    created_at: str | None
    updated_at: str | None
    completed_at: str | None


class PurchaseRequestListResponse(BaseModel):
    items: list[PurchaseRequestResponse]
    total: int
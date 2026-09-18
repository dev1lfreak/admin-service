from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CreateOrganizationRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=512)
    short_name: str | None = Field(default=None, max_length=256)
    inn: str = Field(min_length=10, max_length=12)
    ogrn: str | None = Field(default=None, max_length=15)
    kpp: str | None = Field(default=None, max_length=9)
    legal_address: str | None = None
    actual_address: str | None = None
    bank_details: dict[str, Any] | None = None
    contact_person: str | None = Field(default=None, max_length=256)
    contact_phone: str | None = Field(default=None, max_length=16)
    status: str = 'active'


class UpdateOrganizationRequest(BaseModel):
    name: str | None = Field(default=None, max_length=512)
    short_name: str | None = Field(default=None, max_length=256)
    ogrn: str | None = Field(default=None, max_length=15)
    kpp: str | None = Field(default=None, max_length=9)
    legal_address: str | None = None
    actual_address: str | None = None
    bank_details: dict[str, Any] | None = None
    contact_person: str | None = Field(default=None, max_length=256)
    contact_phone: str | None = Field(default=None, max_length=16)
    status: str | None = None


class OrganizationResponse(BaseModel):
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
    kyc_verified_at: str | None
    has_wallets: bool
    created_by: str | None
    created_at: str | None
    updated_at: str | None


class OrganizationListResponse(BaseModel):
    items: list[OrganizationResponse]
    total: int


class DocumentResponse(BaseModel):
    organization_id: str
    document_type: str
    s3_key: str | None
    file_name: str | None
    content_type: str | None = None
    file_size_bytes: int | None = None
    download_url: str | None = None

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixins import AuditTimestampsMixin, UlidPrimaryKeyMixin


class LegalEntityModel(Base, UlidPrimaryKeyMixin, AuditTimestampsMixin):
    __tablename__ = 'legal_entities'

    user_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(256), nullable=True)
    inn: Mapped[str] = mapped_column(String(12), nullable=False, index=True)
    ogrn: Mapped[str | None] = mapped_column(String(15), nullable=True)
    kpp: Mapped[str | None] = mapped_column(String(9), nullable=True)
    legal_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    actual_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    bank_details: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    contact_person: Mapped[str | None] = mapped_column(String(256), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(16), nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, server_default='active', default='active')
    kyc_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='true', default=True)
    kyc_verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    encrypted_mnemonic: Mapped[str | None] = mapped_column(Text, nullable=True)
    charter_s3_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    inn_certificate_s3_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    ogrn_certificate_s3_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    bank_details_document_s3_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    kyc_representative_s3_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    power_of_attorney_s3_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    other_document_s3_key: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    created_by: Mapped[str | None] = mapped_column(
        String(26),
        ForeignKey('admin_users.id'),
        nullable=True,
    )

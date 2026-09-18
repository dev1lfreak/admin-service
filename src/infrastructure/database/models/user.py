from __future__ import annotations

from sqlalchemy import Boolean, Date, String, DateTime, Text
from sqlalchemy.orm import Mapped,mapped_column
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixins import UlidPrimaryKeyMixin,AuditTimestampsMixin,SoftDeleteMixin


class UserModel(Base, UlidPrimaryKeyMixin, AuditTimestampsMixin, SoftDeleteMixin):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    birth_date: Mapped[Date | None] = mapped_column(Date, nullable=True)

    encrypted_mnemonic: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(16), nullable=True)

    passport_data: Mapped[str | None] = mapped_column(String(255), nullable=True)
    inn: Mapped[str | None] = mapped_column(String(12), nullable=True)
    erc20: Mapped[str | None] = mapped_column(String(255), nullable=True)

    avatar_link: Mapped[str | None] = mapped_column(Text, nullable=True)

    kyc_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false', default=False)
    kyc_verified_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    account_type: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        server_default='individual',
        default='individual',
    )
    provisioned_by: Mapped[str | None] = mapped_column(String(26), nullable=True)
    provisioned_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

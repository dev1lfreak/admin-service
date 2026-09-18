from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixins import AuditTimestampsMixin, UlidPrimaryKeyMixin


class PurchaseRequestModel(Base, UlidPrimaryKeyMixin, AuditTimestampsMixin):
    __tablename__ = 'purchase_requests'

    organization_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('legal_entities.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, server_default='submitted', default='submitted')
    rub_amount: Mapped[Decimal] = mapped_column(Numeric(18, 8), nullable=False)
    usdt_amount: Mapped[Decimal | None] = mapped_column(Numeric(18, 2), nullable=True)
    exchange_rate: Mapped[Decimal | None] = mapped_column(Numeric(18, 8), nullable=True)
    service_fee_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    admin_comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    target_wallet_chain: Mapped[str | None] = mapped_column(String(16), nullable=True, server_default='ETH')
    target_wallet_address: Mapped[str | None] = mapped_column(String(128), nullable=True)
    tx_hash: Mapped[str | None] = mapped_column(String(128), nullable=True)
    assigned_to: Mapped[str | None] = mapped_column(
        String(26),
        ForeignKey('admin_users.id'),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

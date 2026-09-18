from __future__ import annotations
from decimal import Decimal
from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.application.domain.enums import OrderStatus
from src.infrastructure.database.models.base import Base
from src.infrastructure.database.models.mixins import AuditTimestampsMixin, UlidPrimaryKeyMixin


class OrderModel(Base, UlidPrimaryKeyMixin, AuditTimestampsMixin):
    __tablename__ = 'orders'

    user_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
        index=True,
    )
    usdt_amount: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    usdt_exchange_rate: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    gas_fee: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    service_fee: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        SAEnum(OrderStatus,name='order_status_enum',values_callable=lambda x:[e.value for e in x]),
        nullable=False,
        index=True,
        default=OrderStatus.PENDING,
    )

    client_payment_id: Mapped[str] = mapped_column(
        String(26),
        nullable=False,
        unique=True,
        index=True
    )

    itpay_payment_qr_url_desktop: Mapped[str | None] = mapped_column(Text, nullable=True)
    itpay_payment_qr_url_android: Mapped[str | None] = mapped_column(Text, nullable=True)
    itpay_payment_qr_url_ios: Mapped[str | None] = mapped_column(Text, nullable=True)

    itpay_payment_qr_image_desktop: Mapped[str | None] = mapped_column(Text, nullable=True)
    itpay_payment_qr_image_android: Mapped[str | None] = mapped_column(Text, nullable=True)
    itpay_payment_qr_image_ios: Mapped[str | None] = mapped_column(Text, nullable=True)

    itpay_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    itpay_qr_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    itpay_amount: Mapped[Decimal] = mapped_column(Numeric(38, 2), nullable=False)
    itpay_created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )


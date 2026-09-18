from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from src.application.domain.enums import OrderStatus


@dataclass(slots=True)
class OrderEntity:
    id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    user_id: str | None = None
    usdt_amount: Decimal | None = None
    usdt_exchange_rate: Decimal | None = None
    gas_fee: Decimal | None = None
    total_price: Decimal | None = None
    service_fee: Decimal | None = None
    status: OrderStatus | None = None

    client_payment_id: str | None = None

    itpay_payment_qr_url_desktop: str | None = None
    itpay_payment_qr_url_android: str | None = None
    itpay_payment_qr_url_ios: str | None = None

    itpay_payment_qr_image_desktop: str | None = None
    itpay_payment_qr_image_android: str | None = None
    itpay_payment_qr_image_ios: str | None = None

    itpay_id: str | None = None
    itpay_qr_id: str | None = None
    itpay_amount: Decimal | None = None
    itpay_created_at: datetime | None = None


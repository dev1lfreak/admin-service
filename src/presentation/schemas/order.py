from decimal import Decimal
from pydantic import BaseModel
from src.application.domain.enums import OrderStatus


class OrderDetailResponse(BaseModel):
    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    user_id: str | None = None
    usdt_amount: str | None = None
    usdt_exchange_rate: str | None = None
    gas_fee: str | None = None
    total_price: str | None = None
    service_fee: str | None = None
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
    itpay_amount: str | None = None
    itpay_created_at: str | None = None


class OrderResponse(BaseModel):
    order_id: str
    order_status: OrderStatus | None = None
    usdt_amount: str | None = None
    usdt_exchange_rate: str | None = None
    gas_fee: str | None = None
    total_price: str | None = None
    service_fee: str | None = None
    updated_at: str | None = None


class OrdersResponse(BaseModel):
    items: list[OrderResponse]
    total: int

class OrdersByDateResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    summed_service_fees: Decimal
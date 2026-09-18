from decimal import Decimal
from pydantic import BaseModel

class OrderAnalyticsResponse(BaseModel):
    orders_count: list[int]
    summed_service_fees: list[Decimal]
    total_orders: int
    total_summed_service_fees: Decimal
    period: int | None = None


class PurchaseRequestAnalyticsResponse(BaseModel):
    requests_count: list[int]
    total_requests: int
    period: int | None = None
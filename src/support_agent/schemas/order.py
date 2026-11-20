from enum import StrEnum

from pydantic import BaseModel


class OrderStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELED = "canceled"


class OrderResponse(BaseModel):
    order_number: str
    status: OrderStatus
    can_be_canceled: bool

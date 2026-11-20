from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from support_agent.db.base import Base
from support_agent.schemas.order import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        index=True,
    )
    customer_email: Mapped[str] = mapped_column(
        String(320),
        index=True,
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(
            OrderStatus,
            name="order_status",
            values_callable=lambda enum_class: [status.value for status in enum_class],
        ),
        default=OrderStatus.PENDING,
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(
        String(3),
        default="EUR",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

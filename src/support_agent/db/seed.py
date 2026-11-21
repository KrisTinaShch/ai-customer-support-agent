import asyncio
from decimal import Decimal

from sqlalchemy import select

from support_agent.db.session import async_session_factory
from support_agent.models.order import Order
from support_agent.schemas.order import OrderStatus

DEMO_ORDERS = [
    {
        "order_number": "DEMO-1001",
        "customer_email": "maria.demo@example.com",
        "status": OrderStatus.PENDING,
        "total_amount": Decimal("89.90"),
        "currency": "BGN",
    },
    {
        "order_number": "DEMO-1002",
        "customer_email": "maria.demo@example.com",
        "status": OrderStatus.PROCESSING,
        "total_amount": Decimal("249.00"),
        "currency": "BGN",
    },
    {
        "order_number": "DEMO-1003",
        "customer_email": "nikolay.demo@example.com",
        "status": OrderStatus.SHIPPED,
        "total_amount": Decimal("1599.00"),
        "currency": "BGN",
    },
    {
        "order_number": "DEMO-1004",
        "customer_email": "elena.demo@example.com",
        "status": OrderStatus.DELIVERED,
        "total_amount": Decimal("79.50"),
        "currency": "BGN",
    },
    {
        "order_number": "DEMO-1005",
        "customer_email": "georgi.demo@example.com",
        "status": OrderStatus.CANCELED,
        "total_amount": Decimal("310.00"),
        "currency": "BGN",
    },
]


async def seed_orders() -> None:
    async with async_session_factory() as session:
        result = await session.scalars(select(Order.order_number))
        existing_order_numbers = set(result)

        new_orders = [
            Order(**order_data)
            for order_data in DEMO_ORDERS
            if order_data["order_number"] not in existing_order_numbers
        ]

        if not new_orders:
            print("Demo orders already exist.")
            return

        session.add_all(new_orders)
        await session.commit()

        print(f"Added {len(new_orders)} demo orders.")


if __name__ == "__main__":
    asyncio.run(seed_orders())

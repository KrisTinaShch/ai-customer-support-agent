from support_agent.schemas.order import OrderStatus


def can_cancel_order(status: OrderStatus) -> bool:
    return status in (
        OrderStatus.PENDING,
        OrderStatus.PROCESSING,
    )

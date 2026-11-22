from sqlalchemy.ext.asyncio import AsyncSession

from support_agent.models.order import Order
from support_agent.repositories.order import get_order_by_number_for_update
from support_agent.schemas.order import OrderStatus
from support_agent.services.order_rules import can_cancel_order


class ConfirmationRequiredError(Exception):
    pass


class OrderNotFoundError(Exception):
    pass


class CancellationNotAllowedError(Exception):
    pass


async def cancel_order(
    session: AsyncSession, order_number: str, *, confirmed: bool
) -> Order:
    if not confirmed:
        raise ConfirmationRequiredError(
            "Order cancellation requires user confirmation."
        )

    order = await get_order_by_number_for_update(session, order_number)

    if order is None:
        raise OrderNotFoundError("Order not found.")

    if not can_cancel_order(order.status):
        raise CancellationNotAllowedError(
            f"Order with status '{order.status}' cannot be canceled."
        )

    order.status = OrderStatus.CANCELED
    await session.commit()

    return order

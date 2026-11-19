import pytest

from support_agent.schemas.order import OrderStatus
from support_agent.services.order_rules import can_cancel_order


@pytest.mark.parametrize(
    ("status", "expected"),
    [
        (OrderStatus.PENDING, True),
        (OrderStatus.PROCESSING, True),
        (OrderStatus.SHIPPED, False),
        (OrderStatus.DELIVERED, False),
        (OrderStatus.CANCELED, False),
    ],
)
def test_can_cancel_order_for_each_status(
    status: OrderStatus,
    expected: bool,
) -> None:
    assert can_cancel_order(status) is expected

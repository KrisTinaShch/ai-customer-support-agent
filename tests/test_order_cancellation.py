import asyncio
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

import support_agent.services.order_cancellation as cancellation_service
from support_agent.models.order import Order
from support_agent.schemas.order import OrderStatus
from support_agent.services.order_cancellation import (
    CancellationNotAllowedError,
    ConfirmationRequiredError,
)


def test_cancel_order_requires_confirmation(monkeypatch: pytest.MonkeyPatch) -> None:
    find_order = AsyncMock()
    session = AsyncMock(spec=AsyncSession)

    monkeypatch.setattr(
        cancellation_service, "get_order_by_number_for_update", find_order
    )

    with pytest.raises(
        ConfirmationRequiredError,
        match="requires user confirmation",
    ):
        asyncio.run(
            cancellation_service.cancel_order(session, "DEMO-1001", confirmed=False)
        )

    find_order.assert_not_awaited()
    session.commit.assert_not_awaited()


def test_cancel_order_rejects_shipped_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    order = Order(
        order_number="DEMO-1003",
        customer_email="nikolay.demo@example.com",
        status=OrderStatus.SHIPPED,
        total_amount=Decimal("1599.00"),
        currency="BGN",
    )
    find_order = AsyncMock(return_value=order)
    session = AsyncMock(spec=AsyncSession)

    monkeypatch.setattr(
        cancellation_service,
        "get_order_by_number_for_update",
        find_order,
    )

    with pytest.raises(
        CancellationNotAllowedError,
        match="shipped",
    ):
        asyncio.run(
            cancellation_service.cancel_order(
                session,
                "DEMO-1003",
                confirmed=True,
            )
        )

    find_order.assert_awaited_once_with(session, "DEMO-1003")
    assert order.status is OrderStatus.SHIPPED
    session.commit.assert_not_awaited()


def test_cancel_order_changes_status_and_commits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    order = Order(
        order_number="DEMO-1001",
        customer_email="maria.demo@example.com",
        status=OrderStatus.PENDING,
        total_amount=Decimal("89.90"),
        currency="BGN",
    )
    find_order = AsyncMock(return_value=order)
    session = AsyncMock(spec=AsyncSession)

    monkeypatch.setattr(
        cancellation_service,
        "get_order_by_number_for_update",
        find_order,
    )

    result = asyncio.run(
        cancellation_service.cancel_order(
            session,
            "DEMO-1001",
            confirmed=True,
        )
    )

    find_order.assert_awaited_once_with(session, "DEMO-1001")
    assert result is order
    assert order.status is OrderStatus.CANCELED
    session.commit.assert_awaited_once_with()

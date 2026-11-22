from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from support_agent.db.session import get_db_session
from support_agent.repositories.order import get_order_by_number
from support_agent.schemas.order import OrderResponse
from support_agent.services.order_rules import can_cancel_order

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

DatabaseSession = Annotated[AsyncSession, Depends(get_db_session)]


@router.get(
    "/{order_number}",
    response_model=OrderResponse,
)
async def get_order(
    order_number: str,
    session: DatabaseSession,
) -> OrderResponse:
    order = await get_order_by_number(session, order_number)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found."
        )

    return OrderResponse(
        order_number=order.order_number,
        status=order.status,
        can_be_canceled=can_cancel_order(order.status),
    )

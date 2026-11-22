from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from support_agent.db.session import get_db_session
from support_agent.repositories.order import get_order_by_number
from support_agent.schemas.order import OrderCancellationRequest, OrderResponse
from support_agent.services.order_cancellation import (
    CancellationNotAllowedError,
    ConfirmationRequiredError,
    OrderNotFoundError,
)
from support_agent.services.order_cancellation import (
    cancel_order as cancel_order_service,
)
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


@router.post(
    "/{order_number}/cancel",
    response_model=OrderResponse,
)
async def cancel_order(
    order_number: str, request: OrderCancellationRequest, session: DatabaseSession
) -> OrderResponse:
    try:
        order = await cancel_order_service(
            session, order_number, confirmed=request.confirmed
        )
    except ConfirmationRequiredError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except OrderNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except CancellationNotAllowedError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error

    return OrderResponse(
        order_number=order.order_number,
        status=order.status,
        can_be_canceled=can_cancel_order(order.status),
    )

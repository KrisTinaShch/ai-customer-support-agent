from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from support_agent.models.order import Order


async def get_order_by_number(
    session: AsyncSession,
    order_number: str,
) -> Order | None:
    statement = select(Order).where(Order.order_number == order_number)
    result = await session.execute(statement)

    return result.scalar_one_or_none()


async def get_order_by_number_for_update(
    session: AsyncSession,
    order_number: str,
) -> Order | None:
    statement = (
        select(Order).where(Order.order_number == order_number).with_for_update()
    )
    result = await session.execute(statement)

    return result.scalar_one_or_none()

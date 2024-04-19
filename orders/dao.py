from sqlalchemy import desc, select

from base import BaseDAO, async_session_maker
from orders.models import Orders


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def get_by_params(cls, **params):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**params).order_by(desc(cls.model.id))
            result = await session.execute(query)
            return result.scalars().all()

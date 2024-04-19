from sqlalchemy import select
from sqlalchemy.orm import selectinload

from base import BaseDAO, async_session_maker
from foods.models import Categories, Foods


class FoodsDAO(BaseDAO):
    model = Foods

    @classmethod
    async def get_all_foods_with_category(cls):
        async with async_session_maker() as session:
            query = select(cls.model).options(selectinload(cls.model.category))
            result = await session.execute(query)
            return result.scalars().all()


class CategoriesDAO(BaseDAO):
    model = Categories

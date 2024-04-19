from sqlalchemy import delete, insert, select

from database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **params):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**params)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_by_params(cls, **params):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**params)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def delete_all(cls):
        async with async_session_maker() as session:
            query = delete(cls.model)
            await session.execute(query)
            await session.commit()

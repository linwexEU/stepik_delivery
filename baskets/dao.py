from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

from base import BaseDAO, async_session_maker
from baskets.models import Baskets


class BasketsDAO(BaseDAO):
    model = Baskets

    @classmethod
    async def get_basket_with_all_params(cls, user_id):
        async with async_session_maker() as session:
            if user_id:
                query = select(cls.model).options(
                    selectinload(cls.model.user_from_basket),
                    selectinload(cls.model.food_from_basket),
                ).where(cls.model.user_id == user_id)
            else:
                return []

            data = await session.execute(query)

            result = []
            for item in data:
                new_item = {
                    "user_id": item[0].user_id,
                    "food_id": item[0].food_id,
                    "user_from_basket": {
                        "id": item[0].user_from_basket.id,
                        "username": item[0].user_from_basket.username,
                        "email": item[0].user_from_basket.email,
                    },
                    "food_from_basket": {
                        "id": item[0].food_from_basket.id,
                        "name": item[0].food_from_basket.name,
                        "price": item[0].food_from_basket.price,
                    },
                    "buy_count": 1,
                }
                if new_item["food_from_basket"]["name"] not in [
                    item["food_from_basket"]["name"] for item in result
                ]:
                    result.append(new_item)
                else:
                    for indx, c in enumerate(result):
                        if new_item["food_id"] == c["food_id"]:
                            result[indx]["buy_count"] += 1

            return result

    @classmethod
    async def delete_by_food_id(cls, food_id):
        async with async_session_maker() as session:
            query = text("DELETE FROM basket WHERE food_id = :food_id LIMIT 1")
            await session.execute(query, {"food_id": food_id})
            await session.commit()

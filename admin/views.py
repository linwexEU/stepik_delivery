from sqladmin import ModelView

from users.models import Users
from baskets.models import Baskets
from foods.models import Foods, Categories
from orders.models import Orders

from users.auth import get_password_hash


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.username]
    column_details_exclude_list = [Users.hashed_password]

    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    async def on_model_change(self, data: dict, model: Users, is_created: bool) -> None:
        data["hashed_password"] = get_password_hash(data["hashed_password"])


class BasketsAdmin(ModelView, model=Baskets):
    column_list = [Baskets.id, Baskets.user_id, Baskets.food_id]

    name = "Basket"
    name_plural = "Baskets"
    icon = "fa-solid fa-trash"


class FoodsAdmin(ModelView, model=Foods):
    column_list = [
        Foods.id,
        Foods.name,
        Foods.price,
        Foods.description,
        Foods.category_id,
    ]
    column_details_exclude_list = [Foods.image]

    name = "Food"
    name_plural = "Foods"
    icon = "fa-solid fa-burger"


class CategoriesAdmin(ModelView, model=Categories):
    column_list = [Categories.id, Categories.name]

    name = "Category"
    name_plural = "Categories"
    icon = "fa-solid fa-icons"


class OrdersAdmin(ModelView, model=Orders):
    column_list = [
        Orders.id,
        Orders.user_id,
        Orders.data,
        Orders.sum,
        Orders.status,
        Orders.email,
        Orders.phone,
        Orders.address,
        Orders.foods,
    ]

    name = "Order"
    name_plural = "Orders"
    icon = "fa-solid fa-truck-fast"

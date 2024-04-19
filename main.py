from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from account.router import router as router_account
from admin.views import UsersAdmin, BasketsAdmin, FoodsAdmin, CategoriesAdmin, OrdersAdmin
from baskets.router import router as router_basket
from baskets.dao import BasketsDAO
from config import settings
from database import engine
from foods.router import get_foods
from foods.router import router as router_food
from foods.schemas import SFoods
from orders.router import router as router_order
from users.dependencies import get_current_user
from users.router import router as router_user
from message import get_flash_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="redis-cache")
    yield


app = FastAPI(lifespan=lifespan)
admin = Admin(app, engine)
templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flash_message"] = get_flash_message

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(router_user)
app.include_router(router_order)
app.include_router(router_basket)
app.include_router(router_food)
app.include_router(router_account)

admin.add_view(UsersAdmin) 
admin.add_view(BasketsAdmin) 
admin.add_view(FoodsAdmin) 
admin.add_view(CategoriesAdmin) 
admin.add_view(OrdersAdmin) 


@app.exception_handler(StarletteHTTPException)
async def bluescreen_error(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("error.html", {"request": request})


@app.get("/")
async def get_main(
    request: Request,
    foods_data: list[SFoods] = Depends(get_foods),
    user=Depends(get_current_user),
):
    foods = await BasketsDAO.get_basket_with_all_params(user_id=user["Users"].id if user else None)
    full_price = sum(
        [item["buy_count"] * item["food_from_basket"]["price"] for item in foods]
    )
    amount_of_item = sum([item["buy_count"] for item in foods])
    return templates.TemplateResponse(
        "main.html",
        {"request": request, "foods": foods_data, "full_price": full_price, "amount_of_item": str(amount_of_item), "auth": True if user else False},
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from baskets.dao import BasketsDAO
from message import flash, get_flash_message
from orders.dao import OrdersDAO
from users.dependencies import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])
templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flash_message"] = get_flash_message


@router.get("/")
async def render_cart(request: Request, user=Depends(get_current_user)):
    foods = await BasketsDAO.get_basket_with_all_params(user_id=user["Users"].id if user else None)
    full_price = sum(
        [item["buy_count"] * item["food_from_basket"]["price"] for item in foods]
    )
    amount_of_item = sum([item["buy_count"] for item in foods])

    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "foods": foods,
            "full_price": full_price,
            "amount_of_item": amount_of_item,
            "auth": True if user else False,
        },
    )


@router.get("/delete_food_all/")
async def render_delete_food_all(request: Request): 
    await BasketsDAO.delete_all()
    flash(request=request, message="Все блюда удалены из корзины")
    return RedirectResponse("http://127.0.0.1:8000/cart/", status_code=303)


@router.get("/delete_food/{food_id}/")
async def render_delete_food_by_id(request: Request, food_id: int):
    await BasketsDAO.delete_by_food_id(food_id=food_id)
    flash(request=request, message="Блюдо удалено из корзины")
    return RedirectResponse("http://127.0.0.1:8000/cart/", status_code=303)


@router.post("/")
async def render_post_cart(
    request: Request,
    address: Annotated[str, Form(...)],
    email: Annotated[EmailStr, Form(...)],
    phone: Annotated[str | None, Form(...)] = None,
    user=Depends(get_current_user),
):
    if request.method == "POST":
        foods = await BasketsDAO.get_basket_with_all_params(user_id=user["Users"].id if user else None)
        full_price = sum(
            [item["buy_count"] * item["food_from_basket"]["price"] for item in foods]
        )
        if foods == []:
            flash(request, "Корзина пустая")
            return RedirectResponse("/cart/", status_code=303)
        else:
            current_date = datetime.now()
            await OrdersDAO.add(
                user_id=user["Users"].id,
                data=f"{str(current_date.day).rjust(2, '0')}.{str(current_date.month).rjust(2, '0')}.{current_date.year}",
                sum=full_price,
                status="В пути",
                email=email,
                phone=phone,
                address=address,
                foods=[
                    {
                        "food_name": food["food_from_basket"]["name"],
                        "food_price": food["food_from_basket"]["price"],
                        "buy_count": food["buy_count"],
                    }
                    for food in foods
                ],
            )
            await BasketsDAO.delete_all()
            return RedirectResponse("http://127.0.0.1:8000/order/", status_code=303)


@router.post("/addtocart/{food_id}/")
async def render_add_to_cart(request: Request, food_id: int, user=Depends(get_current_user)):
    if request.method == "POST":
        if not user:
            flash(request=request, message="Войти или зарегистрируйтесь для того, чтоб добавлять товар в корзину")
        else:
            await BasketsDAO.add(user_id=user["Users"].id, food_id=food_id)
        return RedirectResponse("http://127.0.0.1:8000/", status_code=303)

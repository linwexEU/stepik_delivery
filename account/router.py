from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates

from baskets.dao import BasketsDAO
from orders.dao import OrdersDAO
from users.dependencies import get_current_user

router = APIRouter(prefix="/account", tags=["Account"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def render_account(request: Request, user=Depends(get_current_user)):
    foods = await BasketsDAO.get_basket_with_all_params(user_id=user["Users"].id if user else None)
    full_price = sum(
            [item["buy_count"] * item["food_from_basket"]["price"] for item in foods]
        )
    amount_of_item = sum([item["buy_count"] for item in foods])
    try:
        orders = await OrdersDAO.get_by_params(user_id=user["Users"].id)
    except:
        raise HTTPException(status_code=401)

    return templates.TemplateResponse(
        "account.html",
        {
            "request": request,
            "orders": orders if orders else [],
            "full_price": full_price, 
            "amount_of_item": amount_of_item,
            "auth": True if user else False,
        },
    )

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates

from users.dependencies import get_current_user

router = APIRouter(prefix="/order", tags=["Orders"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def render_order(request: Request, user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401)

    return templates.TemplateResponse("ordered.html", {"request": request})

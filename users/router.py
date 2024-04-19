from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request, Response, status
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from users.auth import authenticate_user, create_access_token, get_password_hash
from users.dao import UsersDAO

router = APIRouter(prefix="/auth", tags=["Auth & Reg"])
templates = Jinja2Templates(directory="templates")


@router.get("/register/")
async def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register/")
async def render_register(
    username: Annotated[str, Form(...)],
    email: Annotated[EmailStr, Form(...)],
    password: Annotated[str, Form(...)],
):
    user = await UsersDAO.get_by_params(username=username)

    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    hashed_password = get_password_hash(password)
    await UsersDAO.add(username=username, email=email, hashed_password=hashed_password)
    return {"message": "New user was registed!"}


@router.post("/login/")
async def render_login(
    response: Response,
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
):
    user = await authenticate_user(username, password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": str(user["Users"].id)})
    response.set_cookie("access_token", access_token, httponly=True)
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers["Location"] = "/"
    return response


@router.post("/logout/")
async def render_logout(response: Response):
    response.delete_cookie("access_token")
    response.status_code = status.HTTP_303_SEE_OTHER
    response.headers["Location"] = "/"
    return response


@router.get("/login/")
async def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

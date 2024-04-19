import datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from config import settings
from users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return False
    return token


async def get_current_user(token: str | bool = Depends(get_token)):
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        except JWTError:
            return False
        expire: str = payload.get("exp")
        if (not expire) or (
            int(expire) < datetime.datetime.now(datetime.UTC).timestamp()
        ):
            return False
        user_id: str = payload.get("sub")
        if not user_id:
            return False
        user = await UsersDAO.get_by_params(id=int(user_id))
        if not user:
            return False
        return user

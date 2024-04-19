import datetime

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from config import settings
from users.dao import UsersDAO

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=14)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user = await UsersDAO.get_by_params(username=username)
    if not user:
        return False

    if not (user and verify_password(password, user["Users"].hashed_password)):
        return False
    return user

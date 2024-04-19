from pydantic import BaseModel, EmailStr, Field


class SUser(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=1)

from pydantic import BaseModel


class Categories(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class SFoods(BaseModel):
    id: int
    name: str
    price: int
    description: str
    category: Categories

    class Config:
        from_attributes = True

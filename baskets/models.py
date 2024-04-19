from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from users.models import Users # noqa


class Baskets(Base):
    __tablename__ = "basket"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    food_id: Mapped[int] = mapped_column(Integer, ForeignKey("food.id"))

    user_from_basket = relationship("Users", back_populates="basket_from_user")
    food_from_basket = relationship("Foods", back_populates="basket_from_foods")

    def __str__(self): 
        return f"Basket - Food_id-{self.food_id}"
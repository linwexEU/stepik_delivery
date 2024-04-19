from sqlalchemy import ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Foods(Base):
    __tablename__ = "food"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    image: Mapped[bytes] = mapped_column(
        LargeBinary(length=(2**32) - 1), nullable=True
    )
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))

    category = relationship("Categories", back_populates="food")
    basket_from_foods = relationship("Baskets", back_populates="food_from_basket")

    def __str__(self): 
        return self.name
    

class Categories(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)

    food = relationship("Foods", back_populates="category")

    def __str__(self): 
        return self.name
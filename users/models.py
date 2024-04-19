from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Users(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)

    basket_from_user = relationship("Baskets", back_populates="user_from_basket")

    def __str__(self): 
        return f"({self.id}) {self.username}"
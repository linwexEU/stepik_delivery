from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Orders(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    data: Mapped[str] = mapped_column(String(64), nullable=False)
    sum: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    phone: Mapped[str] = mapped_column(String(64), nullable=False)
    address: Mapped[str] = mapped_column(String(64), nullable=False)
    foods: Mapped[str] = mapped_column(JSON, nullable=False)

    def __str__(self): 
        return self.data
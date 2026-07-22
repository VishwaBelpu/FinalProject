from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from dependencies.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    customer = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart")

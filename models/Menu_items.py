from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from dependencies.database import Base

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    name = Column(String(120), nullable=False)
    description = Column(String(500))
    price = Column(DECIMAL(10, 2), nullable=False, server_default="0.0")
    category = Column(String(50))
    available = Column(Integer, nullable=False, server_default="1")

    restaurant = relationship("Restaurant", back_populates="menu_items")
    cart_items = relationship("CartItem", back_populates="menu_items")
    order_items = relationship("OrderItem", back_populates="menu_items")
    reviews = relationship("Review", back_populates="menu_items")

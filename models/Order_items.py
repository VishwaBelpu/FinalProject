from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, FetchedValue
from sqlalchemy.orm import relationship
from dependencies.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id  = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, nullable=False, server_default="1")
    price_at_order = Column(DECIMAL(10, 2), nullable=False)
    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")


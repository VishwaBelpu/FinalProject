from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship
from datetime import datetime
from dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("users.id"))
    promo_code_id = Column(Integer, ForeignKey("promo_codes.id"))
    order_date = Column(DATETIME, nullable=False, server_default=str(datetime.now()))
    status = Column(String(30), nullable=False, server_default="pending")
    total_amount = Column(DECIMAL(10, 2), nullable=False)

    customer = relationship("User", back_populates="orders_placed", foreign_keys=[customer_id])
    staff = relationship("User", back_populates="orders_managed", foreign_keys=[staff_id])
    promo_code = relationship("PromoCode", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    payment = relationship("Payment", back_populates="order", uselist=False)

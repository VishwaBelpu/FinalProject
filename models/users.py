from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dependencies.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, server_default="customer")
    delivery_address = Column(String(255))
    station = Column(String(50))

    cart = relationship("Cart", back_populates="customer", uselist=False)
    orders_placed = relationship("Order", back_populates="customer", foreign_keys="Order.customer_id")
    orders_managed = relationship("Order", back_populates="staff", foreign_keys="Order.staff_id")
    reviews = relationship("Review", back_populates="customer")

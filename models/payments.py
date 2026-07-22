from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy.orm import relationship
from dependencies.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    method = Column(String(30), nullable=False)
    status = Column(String(30), nullable=False, server_default="pending")

    order = relationship("Order", back_populates="payment")

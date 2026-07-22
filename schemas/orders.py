from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from schemas.order_items import OrderItem, OrderItemCreate


class OrderBase(BaseModel):
    customer_id: int
    promo_code_id: Optional[int] = None


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    staff_id: Optional[int] = None


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    staff_id: Optional[int] = None
    order_date: Optional[datetime] = None
    status: str
    total_amount: float
    items: list[OrderItem] = None

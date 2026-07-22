from typing import Optional
from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    method: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[str] = None


class Payment(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str

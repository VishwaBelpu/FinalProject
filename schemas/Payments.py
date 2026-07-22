from typing import Optional
from pydantic import BaseModel

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    status: Optional[str] = None

class Payment(PaymentBase):
    id: int
    status: str

    class ConfigDict:
        from_attributes = True
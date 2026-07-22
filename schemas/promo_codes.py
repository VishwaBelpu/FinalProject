from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PromoCodeBase(BaseModel):
    code: str
    discount_percent: float
    expiry_date: datetime


class PromoCodeCreate(PromoCodeBase):
    pass


class PromoCodeUpdate(BaseModel):
    discount_percent: Optional[float] = None
    expiry_date: Optional[datetime] = None


class PromoCode(PromoCodeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

from typing import Optional
from pydantic import BaseModel, ConfigDict


class RestaurantBase(BaseModel):
    name: str
    address: str


class RestaurantCreate(RestaurantBase):
    pass


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None


class Restaurant(RestaurantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

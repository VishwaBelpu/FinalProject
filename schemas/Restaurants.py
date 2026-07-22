from typing import Optional
from pydantic import BaseModel

class RestaurantBase(BaseModel):
    name: str
    address: str

class RestaurantsCreate(RestaurantBase):
    
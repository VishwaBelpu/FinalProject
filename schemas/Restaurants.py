from typing import Optional
from pydantic import BaseModel

class RestaurantBase(BaseModel):
    name: str
    address: str

class RestaurantsCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None

class Restaurant(RestaurantBase):
    id: int
    
    class ConfigDict:
        from_attibutes = True
from typing import Optional
from pydantic import BaseModel

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    available: int = 1

class MenuItemCreate(MenuItemBase):
    restaurant_id: int

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    available: Optional[int] = 1

class MenuItem(MenuItemBase):
    id: int
    restaurant_id: int

    class ConfigDict:
        from_attributes = True
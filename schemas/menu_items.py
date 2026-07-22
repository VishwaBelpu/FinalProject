from typing import Optional
from pydantic import BaseModel, ConfigDict


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
    available: Optional[int] = None


class MenuItem(MenuItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    restaurant_id: int

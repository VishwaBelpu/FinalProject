from typing import Optional
from pydantic import BaseModel, ConfigDict
from schemas.menu_items import MenuItem


class CartItemBase(BaseModel):
    quantity: int = 1


class CartItemCreate(CartItemBase):
    menu_item_id: int


class CartItemUpdate(BaseModel):
    quantity: Optional[int] = None


class CartItem(CartItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cart_id: int
    menu_item_id: int
    menu_item: MenuItem = None

from typing import Optional
from pydantic import BaseModel
from schemas.Menu_items import MenuItem

class CartItemBase(BaseModel):
    quantity: int = 1

class CartItemCreate(CartItemBase):
    quantity: Optional[int] = None

class CartItem(CartItemBase):
    id: int
    cart_id: int
    menu_item_id: int
    menu_item: MenuItem = None

    class ConfigDict:
        from_attributes = True
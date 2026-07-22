from pydantic import BaseModel
from schemas.Menu_items import MenuItem

class OrderItemBase(BaseModel):
    quantity: int = 1
    price_at_order: float

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    menu_item_id: int
    menu_item: MenuItem = None

    class ConfigDict:
        from_attributes = True
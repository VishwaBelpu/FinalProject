from pydantic import BaseModel, ConfigDict
from schemas.menu_items import MenuItem


class OrderItemBase(BaseModel):
    quantity: int = 1
    price_at_order: float


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = 1


class OrderItem(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    menu_item_id: int
    menu_item: MenuItem = None

from pydantic import BaseModel, ConfigDict
from schemas.cart_items import CartItem


class Cart(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    items: list[CartItem] = None

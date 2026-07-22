from pydantic import BaseModel
from schemas.Cart_items import CartItem

class Cart(BaseModel):
    id: int
    customer_id: int
    items: list[CartItem] = None

    class ConfigDict:
        from_attributes = True
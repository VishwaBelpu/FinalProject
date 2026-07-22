from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import carts as controller
from schemas import cart_items as cart_item_schema
from schemas import carts as schema
from schemas import orders as order_schema
from dependencies.database import get_db

router = APIRouter(
    tags=['Cart'],
    prefix="/customers/{customer_id}/cart"
)


@router.get("/", response_model=schema.Cart)
def view(customer_id: int, db: Session = Depends(get_db)):
    return controller.get_or_create(db, customer_id)


@router.post("/items", response_model=schema.Cart)
def add_item(customer_id: int, request: cart_item_schema.CartItemCreate, db: Session = Depends(get_db)):
    return controller.add_item(db, customer_id, request)


@router.delete("/items/{cart_item_id}", response_model=schema.Cart)
def remove_item(customer_id: int, cart_item_id: int, db: Session = Depends(get_db)):
    return controller.remove_item(db, customer_id, cart_item_id)


@router.post("/checkout", response_model=order_schema.Order)
def checkout(customer_id: int, promo_code_id: Optional[int] = None, db: Session = Depends(get_db)):
    return controller.checkout(db, customer_id, promo_code_id)

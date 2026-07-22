from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import orders as controller
from schemas import orders as schema
from dependencies.database import get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.get("/", response_model=list[schema.Order])
def read_all(order_status: Optional[str] = None, db: Session = Depends(get_db)):
    return controller.read_all(db, order_status=order_status)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

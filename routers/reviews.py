from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import reviews as controller
from schemas import reviews as schema
from dependencies.database import get_db

router = APIRouter(
    tags=['Reviews'],
    prefix="/reviews"
)


@router.post("/", response_model=schema.Review)
def create(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/menu-item/{menu_item_id}", response_model=list[schema.Review])
def read_all_for_item(menu_item_id: int, db: Session = Depends(get_db)):
    return controller.read_all_for_item(db, menu_item_id=menu_item_id)

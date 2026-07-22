from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import restaurants as controller
from schemas import restaurants as schema
from dependencies.database import get_db

router = APIRouter(
    tags=['Restaurants'],
    prefix="/restaurants"
)


@router.post("/", response_model=schema.Restaurant)
def create(request: schema.RestaurantCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Restaurant])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Restaurant)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Restaurant)
def update(item_id: int, request: schema.RestaurantUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

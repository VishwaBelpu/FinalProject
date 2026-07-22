from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import promo_codes as controller
from schemas import promo_codes as schema
from dependencies.database import get_db

router = APIRouter(
    tags=['Promo Codes'],
    prefix="/promo-codes"
)


@router.post("/", response_model=schema.PromoCode)
def create(request: schema.PromoCodeCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/{code}", response_model=schema.PromoCode)
def read_one(code: str, db: Session = Depends(get_db)):
    return controller.read_one_by_code(db, code=code)

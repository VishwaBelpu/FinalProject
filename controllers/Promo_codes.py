from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import promo_codes as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    if db.query(model.PromoCode).filter(model.PromoCode.code == request.code).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Promo code already exists")

    new_item = model.PromoCode(
        code=request.code,
        discount_percent=request.discount_percent,
        expiry_date=request.expiry_date,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_one_by_code(db: Session, code):
    try:
        item = db.query(model.PromoCode).filter(model.PromoCode.code == code).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promo code not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

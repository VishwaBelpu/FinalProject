from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import reviews as model
from models import users as user_model
from models import menu_items as menu_item_model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    if not db.query(user_model.User).filter(user_model.User.id == request.customer_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    if not db.query(menu_item_model.MenuItem).filter(menu_item_model.MenuItem.id == request.menu_item_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

    new_item = model.Review(
        customer_id=request.customer_id,
        menu_item_id=request.menu_item_id,
        rating=request.rating,
        comment=request.comment,
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_all_for_item(db: Session, menu_item_id):
    try:
        result = db.query(model.Review).filter(model.Review.menu_item_id == menu_item_id).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result
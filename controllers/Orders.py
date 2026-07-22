from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import orders as model
from models import users as user_model
from sqlalchemy.exc import SQLAlchemyError


def read_all(db: Session, order_status=None):
    try:
        query = db.query(model.Order)
        if order_status:
            query = query.filter(model.Order.status == order_status)
        result = query.order_by(model.Order.order_date.asc()).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        update_data = request.dict(exclude_unset=True)
        if update_data.get("staff_id") is not None:
            if not db.query(user_model.User).filter(user_model.User.id == update_data["staff_id"]).first():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff user not found")

        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()

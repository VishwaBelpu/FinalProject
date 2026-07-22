from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import payments as model
from models import orders as order_model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    order = db.query(order_model.Order).filter(order_model.Order.id == request.order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.payment:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Order already has a payment")

    new_item = model.Payment(
        order_id=request.order_id,
        amount=request.amount,
        method=request.method,
        status="completed",
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Payment).filter(model.Payment.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Payment).filter(model.Payment.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()
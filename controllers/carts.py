from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import carts as cart_model
from models import cart_items as cart_item_model
from models import menu_items as menu_item_model
from models import users as user_model
from models import orders as order_model
from models import order_items as order_item_model
from sqlalchemy.exc import SQLAlchemyError


def get_or_create(db: Session, customer_id):
    if not db.query(user_model.User).filter(user_model.User.id == customer_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    cart = db.query(cart_model.Cart).filter(cart_model.Cart.customer_id == customer_id).first()
    if not cart:
        cart = cart_model.Cart(customer_id=customer_id)
        try:
            db.add(cart)
            db.commit()
            db.refresh(cart)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return cart


def add_item(db: Session, customer_id, request):
    cart = get_or_create(db, customer_id)

    menu_item = db.query(menu_item_model.MenuItem).filter(
        menu_item_model.MenuItem.id == request.menu_item_id
    ).first()
    if not menu_item or not menu_item.available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not available")

    existing = db.query(cart_item_model.CartItem).filter(
        cart_item_model.CartItem.cart_id == cart.id,
        cart_item_model.CartItem.menu_item_id == request.menu_item_id,
    ).first()

    try:
        if existing:
            existing.quantity += request.quantity
        else:
            db.add(cart_item_model.CartItem(
                cart_id=cart.id,
                menu_item_id=request.menu_item_id,
                quantity=request.quantity,
            ))
        db.commit()
        db.refresh(cart)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return cart


def remove_item(db: Session, customer_id, cart_item_id):
    cart = get_or_create(db, customer_id)

    item = db.query(cart_item_model.CartItem).filter(cart_item_model.CartItem.id == cart_item_id).first()
    if not item or item.cart_id != cart.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    try:
        db.delete(item)
        db.commit()
        db.refresh(cart)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return cart


def checkout(db: Session, customer_id, promo_code_id=None):
    cart = get_or_create(db, customer_id)
    if not cart.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    order_items = []
    total = 0.0
    for cart_item in cart.items:
        price = float(cart_item.menu_item.price)
        total += price * cart_item.quantity
        order_items.append(order_item_model.OrderItem(
            menu_item_id=cart_item.menu_item_id,
            quantity=cart_item.quantity,
            price_at_order=price,
        ))

    new_order = order_model.Order(
        customer_id=customer_id,
        promo_code_id=promo_code_id,
        total_amount=total,
        items=order_items,
    )

    try:
        db.add(new_order)
        for cart_item in list(cart.items):
            db.delete(cart_item)
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order

from models import users, restaurants, menu_items, carts, cart_items, orders, order_items, payments, reviews, promo_codes

from dependencies.database import engine


def index():
    users.Base.metadata.create_all(engine)
    restaurants.Base.metadata.create_all(engine)
    menu_items.Base.metadata.create_all(engine)
    carts.Base.metadata.create_all(engine)
    cart_items.Base.metadata.create_all(engine)
    orders.Base.metadata.create_all(engine)
    order_items.Base.metadata.create_all(engine)
    payments.Base.metadata.create_all(engine)
    reviews.Base.metadata.create_all(engine)
    promo_codes.Base.metadata.create_all(engine)

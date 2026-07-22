from models import Users, Restaurants, Menu_items, Carts, Cart_items, Orders, Order_items, Payments, Reviews, Promo_codes

from dependencies.database import engine


def index():
    Users.Base.metadata.create_all(engine)
    Restaurants.Base.metadata.create_all(engine)
    Menu_items.Base.metadata.create_all(engine)
    Carts.Base.metadata.create_all(engine)
    Cart_items.Base.metadata.create_all(engine)
    Orders.Base.metadata.create_all(engine)
    Order_items.Base.metadata.create_all(engine)
    Payments.Base.metadata.create_all(engine)
    Reviews.Base.metadata.create_all(engine)
    Promo_codes.Base.metadata.create_all(engine)

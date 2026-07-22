from routers import users, restaurants, menu_items, carts, orders, payments, reviews, promo_codes


def load_routes(app):
    app.include_router(users.router)
    app.include_router(restaurants.router)
    app.include_router(menu_items.router)
    app.include_router(carts.router)
    app.include_router(orders.router)
    app.include_router(payments.router)
    app.include_router(reviews.router)
    app.include_router(promo_codes.router)

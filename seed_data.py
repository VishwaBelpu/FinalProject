"""
Populates the database with sample data for demoing the Online Restaurant
Ordering System: two restaurants, a full menu each, a handful of users
(customers, staff, admin), a couple of completed orders with payments and
reviews, an order still in the pipeline for demoing staff status updates,
an active shopping cart for demoing checkout live, and two promo codes.

Run this once after the tables exist:
    python seed_data.py
"""

from datetime import datetime, timedelta

from dependencies.database import SessionLocal
from models import model_loader
from models.users import User
from models.restaurants import Restaurant
from models.menu_items import MenuItem
from models.carts import Cart
from models.cart_items import CartItem
from models.orders import Order
from models.order_items import OrderItem
from models.payments import Payment
from models.reviews import Review
from models.promo_codes import PromoCode


def seed(db):
    # Safe to re-run: if the seed data is already there, skip instead of
    # hitting a duplicate-key error on unique columns like users.email.
    if db.query(User).filter(User.email == "ada@example.com").first():
        print("Seed data already present — skipping. "
              "Delete the rows (or drop/recreate the database) if you want to reseed from scratch.")
        return

    # ---- Restaurants -----------------------------------------------------
    bella_italia = Restaurant(name="Bella Italia", address="123 Main St, Raleigh, NC")
    dragon_wok = Restaurant(name="Dragon Wok", address="456 Elm St, Raleigh, NC")
    db.add_all([bella_italia, dragon_wok])
    db.commit()

    # ---- Menu items ---------------------------------------------------
    italia_items = [
        MenuItem(restaurant_id=bella_italia.id, name="Margherita Pizza", description="Tomato, mozzarella, basil", price=12.99, category="Pizza", available=1),
        MenuItem(restaurant_id=bella_italia.id, name="Spaghetti Carbonara", description="Egg, pancetta, parmesan", price=14.50, category="Entree", available=1),
        MenuItem(restaurant_id=bella_italia.id, name="Caesar Salad", description="Romaine, croutons, parmesan", price=8.99, category="Salad", available=1),
        MenuItem(restaurant_id=bella_italia.id, name="Garlic Bread", description="Toasted baguette, garlic butter", price=4.99, category="Appetizer", available=1),
        MenuItem(restaurant_id=bella_italia.id, name="Tiramisu", description="Espresso-soaked ladyfingers, mascarpone", price=6.50, category="Dessert", available=1),
    ]
    wok_items = [
        MenuItem(restaurant_id=dragon_wok.id, name="Kung Pao Chicken", description="Chicken, peanuts, chili peppers", price=13.99, category="Entree", available=1),
        MenuItem(restaurant_id=dragon_wok.id, name="Vegetable Fried Rice", description="Wok-fried rice, mixed vegetables", price=9.99, category="Entree", available=1),
        MenuItem(restaurant_id=dragon_wok.id, name="Spring Rolls", description="Crispy vegetable rolls, sweet chili sauce", price=5.99, category="Appetizer", available=1),
        MenuItem(restaurant_id=dragon_wok.id, name="Hot & Sour Soup", description="Tofu, mushroom, bamboo shoots", price=4.50, category="Soup", available=1),
        MenuItem(restaurant_id=dragon_wok.id, name="Mango Pudding", description="Chilled mango custard", price=5.00, category="Dessert", available=1),
    ]
    db.add_all(italia_items + wok_items)
    db.commit()

    # ---- Users ------------------------------------------------------------
    ada = User(name="Ada Lovelace", email="ada@example.com", password_hash="hashed_pw_1", role="customer", delivery_address="12 Analytical Engine Ave, Raleigh, NC")
    grace = User(name="Grace Hopper", email="grace@example.com", password_hash="hashed_pw_2", role="customer", delivery_address="99 Compiler Ct, Raleigh, NC")
    alan = User(name="Alan Turing", email="alan@example.com", password_hash="hashed_pw_3", role="customer", delivery_address="7 Enigma Way, Raleigh, NC")
    marie = User(name="Marie Curie", email="marie@example.com", password_hash="hashed_pw_4", role="staff", station="Kitchen")
    linus = User(name="Linus Torvalds", email="linus@example.com", password_hash="hashed_pw_5", role="admin")
    db.add_all([ada, grace, alan, marie, linus])
    db.commit()

    # ---- Promo codes --------------------------------------------------
    welcome10 = PromoCode(code="WELCOME10", discount_percent=10.00, expiry_date=datetime.now() + timedelta(days=180))
    summer20 = PromoCode(code="SUMMER20", discount_percent=20.00, expiry_date=datetime.now() + timedelta(days=14))
    db.add_all([welcome10, summer20])
    db.commit()

    # ---- Completed order: Grace, delivered + paid -------------------------
    pizza = italia_items[0]
    tiramisu = italia_items[4]
    order1 = Order(
        customer_id=grace.id,
        staff_id=marie.id,
        order_date=datetime.now() - timedelta(days=2),
        status="delivered",
        total_amount=float(pizza.price) * 2 + float(tiramisu.price),
        items=[
            OrderItem(menu_item_id=pizza.id, quantity=2, price_at_order=pizza.price),
            OrderItem(menu_item_id=tiramisu.id, quantity=1, price_at_order=tiramisu.price),
        ],
    )
    db.add(order1)
    db.commit()
    db.add(Payment(order_id=order1.id, amount=order1.total_amount, method="credit_card", status="completed"))
    db.add(Review(customer_id=grace.id, menu_item_id=pizza.id, rating=5, comment="Best pizza in town!"))
    db.commit()

    # ---- In-progress order: Alan, preparing + paid -------------------
    kung_pao = wok_items[0]
    spring_rolls = wok_items[2]
    order2 = Order(
        customer_id=alan.id,
        staff_id=marie.id,
        order_date=datetime.now() - timedelta(hours=1),
        status="preparing",
        total_amount=float(kung_pao.price) + float(spring_rolls.price),
        items=[
            OrderItem(menu_item_id=kung_pao.id, quantity=1, price_at_order=kung_pao.price),
            OrderItem(menu_item_id=spring_rolls.id, quantity=1, price_at_order=spring_rolls.price),
        ],
    )
    db.add(order2)
    db.commit()
    db.add(Payment(order_id=order2.id, amount=order2.total_amount, method="paypal", status="completed"))
    db.add(Review(customer_id=alan.id, menu_item_id=kung_pao.id, rating=4, comment="Great flavor, a bit spicy for me."))
    db.commit()

    # ---- Fresh order: Grace, still pending -> demo staff status update ----
    fried_rice = wok_items[1]
    order3 = Order(
        customer_id=grace.id,
        order_date=datetime.now(),
        status="pending",
        total_amount=float(fried_rice.price),
        items=[OrderItem(menu_item_id=fried_rice.id, quantity=1, price_at_order=fried_rice.price)],
    )
    db.add(order3)
    db.commit()

    # ---- Active cart: Ada -> demo add-to-cart / checkout live -------------
    carbonara = italia_items[1]
    salad = italia_items[2]
    cart = Cart(customer_id=ada.id)
    db.add(cart)
    db.commit()
    db.add_all([
        CartItem(cart_id=cart.id, menu_item_id=carbonara.id, quantity=1),
        CartItem(cart_id=cart.id, menu_item_id=salad.id, quantity=1),
    ])
    db.commit()

    print("Seed data created:")
    print(f"  Restaurants: {bella_italia.name}, {dragon_wok.name}")
    print(f"  Menu items:  {len(italia_items) + len(wok_items)}")
    print(f"  Users:       {ada.email}, {grace.email}, {alan.email} (customers), {marie.email} (staff), {linus.email} (admin)")
    print(f"  Promo codes: {welcome10.code}, {summer20.code}")
    print(f"  Orders:      #{order1.id} delivered, #{order2.id} preparing, #{order3.id} pending")
    print(f"  Active cart: customer {ada.email} has {len(cart.items)} items ready for checkout demo")


if __name__ == "__main__":
    model_loader.index()
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
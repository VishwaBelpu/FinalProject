from fastapi import HTTPException
import pytest
from controllers import carts as controller
from models import carts as cart_model
from models import users as user_model
from models import cart_items as cart_item_model
from schemas import cart_items as schema


def test_get_or_create_creates_new_cart_for_existing_customer(db_session):
    # Customer exists, but has no cart yet.
    db_session.query.return_value.filter.return_value.first.side_effect = [
        user_model.User(id=1, name="Ada", email="ada@example.com", role="customer"),  # customer lookup
        None,  # no existing cart
    ]

    cart = controller.get_or_create(db_session, customer_id=1)

    assert cart is not None
    assert cart.customer_id == 1
    db_session.add.assert_called_once_with(cart)
    db_session.commit.assert_called_once()


def test_get_or_create_returns_existing_cart(db_session):
    existing = cart_model.Cart(id=4, customer_id=1)
    db_session.query.return_value.filter.return_value.first.side_effect = [
        user_model.User(id=1),
        existing,
    ]

    assert controller.get_or_create(db_session, 1) is existing
    db_session.add.assert_not_called()


def test_get_or_create_rejects_missing_customer(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.get_or_create(db_session, 99)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Customer not found"


def test_add_item_increments_existing_cart_item(mocker):
    db_session = mocker.Mock()
    existing_item = cart_item_model.CartItem(id=1, cart_id=1, menu_item_id=5, quantity=1)

    mocker.patch.object(
        controller, "get_or_create", return_value=mocker.Mock(id=1, items=[existing_item])
    )
    menu_item = mocker.Mock(available=1)
    db_session.query.return_value.filter.return_value.first.side_effect = [menu_item, existing_item]

    request = schema.CartItemCreate(menu_item_id=5, quantity=2)
    controller.add_item(db_session, customer_id=1, request=request)

    assert existing_item.quantity == 3
    db_session.commit.assert_called_once()


def test_add_item_creates_new_cart_item(db_session, mocker):
    cart = mocker.Mock(id=1)
    mocker.patch.object(controller, "get_or_create", return_value=cart)
    db_session.query.return_value.filter.return_value.first.side_effect = [
        mocker.Mock(available=1),
        None,
    ]

    result = controller.add_item(
        db_session, 1, schema.CartItemCreate(menu_item_id=5, quantity=2)
    )

    assert result is cart
    added = db_session.add.call_args.args[0]
    assert added.cart_id == 1
    assert added.menu_item_id == 5
    assert added.quantity == 2


@pytest.mark.parametrize("menu_item", [None, pytest.param(type("Item", (), {"available": 0})(), id="unavailable")])
def test_add_item_rejects_missing_or_unavailable_menu_item(
    db_session, mocker, menu_item
):
    mocker.patch.object(controller, "get_or_create", return_value=mocker.Mock(id=1))
    db_session.query.return_value.filter.return_value.first.return_value = menu_item

    with pytest.raises(HTTPException) as exc:
        controller.add_item(
            db_session, 1, schema.CartItemCreate(menu_item_id=5, quantity=1)
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "Menu item not available"


def test_remove_item(db_session, mocker):
    cart = mocker.Mock(id=1)
    item = cart_item_model.CartItem(id=3, cart_id=1, menu_item_id=5, quantity=1)
    mocker.patch.object(controller, "get_or_create", return_value=cart)
    db_session.query.return_value.filter.return_value.first.return_value = item

    assert controller.remove_item(db_session, 1, 3) is cart
    db_session.delete.assert_called_once_with(item)


def test_remove_item_rejects_item_from_another_cart(db_session, mocker):
    mocker.patch.object(controller, "get_or_create", return_value=mocker.Mock(id=1))
    db_session.query.return_value.filter.return_value.first.return_value = (
        cart_item_model.CartItem(id=3, cart_id=2)
    )

    with pytest.raises(HTTPException) as exc:
        controller.remove_item(db_session, 1, 3)
    assert exc.value.status_code == 404


def test_checkout_builds_order_and_empties_cart(db_session, mocker):
    first = mocker.Mock(menu_item_id=5, quantity=2)
    first.menu_item.price = 4.50
    second = mocker.Mock(menu_item_id=6, quantity=1)
    second.menu_item.price = 3.00
    cart = mocker.Mock(items=[first, second])
    mocker.patch.object(controller, "get_or_create", return_value=cart)

    order = controller.checkout(db_session, customer_id=1, promo_code_id=8)

    assert order.customer_id == 1
    assert order.promo_code_id == 8
    assert float(order.total_amount) == 12.0
    assert [(i.menu_item_id, i.quantity, float(i.price_at_order)) for i in order.items] == [
        (5, 2, 4.5),
        (6, 1, 3.0),
    ]
    db_session.add.assert_called_once_with(order)
    assert db_session.delete.call_count == 2


def test_checkout_rejects_empty_cart(db_session, mocker):
    mocker.patch.object(
        controller, "get_or_create", return_value=mocker.Mock(items=[])
    )
    with pytest.raises(HTTPException) as exc:
        controller.checkout(db_session, customer_id=1)
    assert exc.value.status_code == 400
    assert exc.value.detail == "Cart is empty"

import pytest
from controllers import carts as controller
from models import users as user_model
from models import cart_items as cart_item_model
from schemas import cart_items as schema


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_get_or_create_creates_new_cart_for_existing_customer(db_session):
    # Customer exists, but has no cart yet.
    db_session.query.return_value.filter.return_value.first.side_effect = [
        user_model.User(id=1, name="Ada", email="ada@example.com", role="customer"),  # customer lookup
        None,  # no existing cart
    ]

    cart = controller.get_or_create(db_session, customer_id=1)

    assert cart is not None
    assert cart.customer_id == 1


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

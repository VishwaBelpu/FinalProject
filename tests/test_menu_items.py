import pytest
from controllers import menu_items as controller
from schemas import menu_items as schema


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_menu_item(db_session):
    request = schema.MenuItemCreate(
        restaurant_id=1, name="Carbonara", price=14.5, category="Entree"
    )

    created_item = controller.create(db_session, request)

    assert created_item is not None
    assert created_item.name == "Carbonara"
    assert created_item.price == 14.5
    assert created_item.restaurant_id == 1
    assert created_item.available == 1

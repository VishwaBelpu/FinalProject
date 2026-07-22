import pytest
from controllers import restaurants as controller
from schemas import restaurants as schema


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_restaurant(db_session):
    request = schema.RestaurantCreate(name="Pasta Place", address="456 Oak Ave")

    created_restaurant = controller.create(db_session, request)

    assert created_restaurant is not None
    assert created_restaurant.name == "Pasta Place"
    assert created_restaurant.address == "456 Oak Ave"

from fastapi import HTTPException
import pytest
from controllers import restaurants as controller
from schemas import restaurants as schema


def test_create_restaurant(db_session):
    request = schema.RestaurantCreate(name="Pasta Place", address="456 Oak Ave")

    created_restaurant = controller.create(db_session, request)

    assert created_restaurant is not None
    assert created_restaurant.name == "Pasta Place"
    assert created_restaurant.address == "456 Oak Ave"
    db_session.add.assert_called_once_with(created_restaurant)
    db_session.commit.assert_called_once()


def test_read_all_restaurants(db_session):
    expected = [object()]
    db_session.query.return_value.all.return_value = expected
    assert controller.read_all(db_session) is expected


def test_read_one_restaurant(db_session):
    expected = object()
    db_session.query.return_value.filter.return_value.first.return_value = expected
    assert controller.read_one(db_session, 1) is expected


def test_read_one_restaurant_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.read_one(db_session, 1)
    assert exc.value.status_code == 404


def test_update_restaurant(db_session):
    query = db_session.query.return_value.filter.return_value
    updated = object()
    query.first.side_effect = [object(), updated]

    result = controller.update(
        db_session, 1, schema.RestaurantUpdate(address="789 Elm St")
    )

    assert result is updated
    query.update.assert_called_once_with(
        {"address": "789 Elm St"}, synchronize_session=False
    )
    db_session.commit.assert_called_once()


def test_update_restaurant_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.update(db_session, 1, schema.RestaurantUpdate(name="Missing"))
    assert exc.value.status_code == 404


def test_delete_restaurant(db_session):
    query = db_session.query.return_value.filter.return_value
    query.first.return_value = object()

    response = controller.delete(db_session, 1)

    assert response.status_code == 204
    query.delete.assert_called_once_with(synchronize_session=False)


def test_delete_restaurant_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.delete(db_session, 1)
    assert exc.value.status_code == 404

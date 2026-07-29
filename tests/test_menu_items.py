from fastapi import HTTPException
import pytest
from controllers import menu_items as controller
from schemas import menu_items as schema


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
    db_session.add.assert_called_once_with(created_item)


def test_read_all_menu_items_without_filters(db_session):
    expected = [object()]
    db_session.query.return_value.all.return_value = expected
    assert controller.read_all(db_session) is expected
    db_session.query.return_value.filter.assert_not_called()


def test_read_all_menu_items_with_category_and_search(db_session):
    query = db_session.query.return_value
    filtered_once = query.filter.return_value
    filtered_twice = filtered_once.filter.return_value
    expected = [object()]
    filtered_twice.all.return_value = expected

    assert controller.read_all(db_session, category="Entree", search="carb") is expected
    query.filter.assert_called_once()
    filtered_once.filter.assert_called_once()


def test_read_one_menu_item(db_session):
    expected = object()
    db_session.query.return_value.filter.return_value.first.return_value = expected
    assert controller.read_one(db_session, 5) is expected


def test_read_one_menu_item_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.read_one(db_session, 5)
    assert exc.value.status_code == 404


def test_update_menu_item(db_session):
    query = db_session.query.return_value.filter.return_value
    updated = object()
    query.first.side_effect = [object(), updated]

    result = controller.update(
        db_session, 5, schema.MenuItemUpdate(price=16.25, available=0)
    )

    assert result is updated
    query.update.assert_called_once_with(
        {"price": 16.25, "available": 0}, synchronize_session=False
    )


def test_update_menu_item_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.update(db_session, 5, schema.MenuItemUpdate(price=1))
    assert exc.value.status_code == 404


def test_delete_menu_item(db_session):
    query = db_session.query.return_value.filter.return_value
    query.first.return_value = object()
    response = controller.delete(db_session, 5)
    assert response.status_code == 204
    query.delete.assert_called_once_with(synchronize_session=False)


def test_delete_menu_item_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.delete(db_session, 5)
    assert exc.value.status_code == 404

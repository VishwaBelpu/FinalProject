from fastapi import HTTPException
import pytest

from controllers import orders as controller
from schemas import orders as schema


def test_read_all_orders(db_session):
    query = db_session.query.return_value
    ordered = query.order_by.return_value
    expected = [object(), object()]
    ordered.all.return_value = expected

    assert controller.read_all(db_session) is expected
    query.filter.assert_not_called()


def test_read_all_orders_filters_by_status(db_session):
    query = db_session.query.return_value
    filtered = query.filter.return_value
    expected = [object()]
    filtered.order_by.return_value.all.return_value = expected

    assert controller.read_all(db_session, order_status="pending") is expected
    query.filter.assert_called_once()


def test_read_one_order(db_session):
    expected = object()
    db_session.query.return_value.filter.return_value.first.return_value = expected
    assert controller.read_one(db_session, 4) is expected


def test_read_one_order_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.read_one(db_session, 4)
    assert exc.value.status_code == 404


def test_update_order_status(db_session):
    order_query = db_session.query.return_value.filter.return_value
    updated = object()
    order_query.first.side_effect = [object(), updated]

    result = controller.update(
        db_session, 4, schema.OrderUpdate(status="preparing")
    )

    assert result is updated
    order_query.update.assert_called_once_with(
        {"status": "preparing"}, synchronize_session=False
    )


def test_update_order_assigns_existing_staff(db_session):
    order_query = db_session.query.return_value.filter.return_value
    order_query.first.side_effect = [object(), object(), object()]

    controller.update(db_session, 4, schema.OrderUpdate(staff_id=9))

    order_query.update.assert_called_once_with(
        {"staff_id": 9}, synchronize_session=False
    )


def test_update_order_rejects_missing_staff(db_session):
    filters = db_session.query.return_value.filter.return_value
    filters.first.side_effect = [object(), None]

    with pytest.raises(HTTPException) as exc:
        controller.update(db_session, 4, schema.OrderUpdate(staff_id=99))

    assert exc.value.status_code == 404
    assert exc.value.detail == "Staff user not found"


def test_update_order_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.update(db_session, 99, schema.OrderUpdate(status="ready"))
    assert exc.value.status_code == 404

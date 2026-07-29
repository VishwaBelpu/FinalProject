from fastapi import HTTPException
import pytest

from controllers import payments as controller
from schemas import payments as schema


def test_create_payment(db_session, mocker):
    order = mocker.Mock(payment=None)
    db_session.query.return_value.filter.return_value.first.return_value = order
    request = schema.PaymentCreate(order_id=3, amount=24.5, method="card")

    payment = controller.create(db_session, request)

    assert payment.order_id == 3
    assert float(payment.amount) == 24.5
    assert payment.method == "card"
    assert payment.status == "completed"
    db_session.add.assert_called_once_with(payment)


def test_create_payment_rejects_missing_order(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    request = schema.PaymentCreate(order_id=99, amount=24.5, method="card")

    with pytest.raises(HTTPException) as exc:
        controller.create(db_session, request)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Order not found"


def test_create_payment_rejects_second_payment(db_session, mocker):
    db_session.query.return_value.filter.return_value.first.return_value = (
        mocker.Mock(payment=object())
    )
    request = schema.PaymentCreate(order_id=3, amount=24.5, method="card")

    with pytest.raises(HTTPException) as exc:
        controller.create(db_session, request)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Order already has a payment"


def test_read_one_payment(db_session):
    expected = object()
    db_session.query.return_value.filter.return_value.first.return_value = expected
    assert controller.read_one(db_session, 2) is expected


def test_read_one_payment_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.read_one(db_session, 2)
    assert exc.value.status_code == 404


def test_update_payment(db_session):
    query = db_session.query.return_value.filter.return_value
    updated = object()
    query.first.side_effect = [object(), updated]

    result = controller.update(
        db_session, 2, schema.PaymentUpdate(status="refunded")
    )

    assert result is updated
    query.update.assert_called_once_with(
        {"status": "refunded"}, synchronize_session=False
    )


def test_update_payment_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.update(db_session, 2, schema.PaymentUpdate(status="failed"))
    assert exc.value.status_code == 404

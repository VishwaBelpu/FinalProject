from fastapi import HTTPException
import pytest
from controllers import promo_codes as controller
from models import promo_codes as promo_model
from schemas import promo_codes as schema


def test_create_promo_code(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    request = schema.PromoCodeCreate(code="SAVE10", discount_percent=10, expiry_date="2026-12-31T00:00:00")

    created_promo = controller.create(db_session, request)

    assert created_promo is not None
    assert created_promo.code == "SAVE10"
    assert float(created_promo.discount_percent) == 10.0
    db_session.add.assert_called_once_with(created_promo)


def test_create_duplicate_promo_code(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = (
        promo_model.PromoCode(code="SAVE10")
    )
    request = schema.PromoCodeCreate(
        code="SAVE10", discount_percent=10, expiry_date="2026-12-31T00:00:00"
    )

    with pytest.raises(HTTPException) as exc:
        controller.create(db_session, request)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Promo code already exists"
    db_session.add.assert_not_called()


def test_read_promo_code_by_code(db_session):
    expected = object()
    db_session.query.return_value.filter.return_value.first.return_value = expected
    assert controller.read_one_by_code(db_session, "SAVE10") is expected


def test_read_promo_code_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        controller.read_one_by_code(db_session, "MISSING")
    assert exc.value.status_code == 404
    assert exc.value.detail == "Promo code not found"

import pytest
from controllers import promo_codes as controller
from schemas import promo_codes as schema


@pytest.fixture
def db_session(mocker):
    session = mocker.Mock()
    # No existing promo code with this code, so create() doesn't reject it as a duplicate.
    session.query.return_value.filter.return_value.first.return_value = None
    return session


def test_create_promo_code(db_session):
    request = schema.PromoCodeCreate(code="SAVE10", discount_percent=10, expiry_date="2026-12-31T00:00:00")

    created_promo = controller.create(db_session, request)

    assert created_promo is not None
    assert created_promo.code == "SAVE10"
    assert float(created_promo.discount_percent) == 10.0

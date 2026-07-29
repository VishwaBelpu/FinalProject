from fastapi import HTTPException
import pytest

from controllers import reviews as controller
from schemas import reviews as schema


def review_request():
    return schema.ReviewCreate(
        customer_id=1, menu_item_id=5, rating=4, comment="Very good"
    )


def test_create_review(db_session):
    db_session.query.return_value.filter.return_value.first.side_effect = [
        object(),
        object(),
    ]

    review = controller.create(db_session, review_request())

    assert review.customer_id == 1
    assert review.menu_item_id == 5
    assert review.rating == 4
    assert review.comment == "Very good"
    db_session.add.assert_called_once_with(review)


def test_create_review_rejects_missing_customer(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        controller.create(db_session, review_request())

    assert exc.value.status_code == 404
    assert exc.value.detail == "Customer not found"


def test_create_review_rejects_missing_menu_item(db_session):
    db_session.query.return_value.filter.return_value.first.side_effect = [
        object(),
        None,
    ]

    with pytest.raises(HTTPException) as exc:
        controller.create(db_session, review_request())

    assert exc.value.status_code == 404
    assert exc.value.detail == "Menu item not found"


def test_read_all_reviews_for_item(db_session):
    expected = [object(), object()]
    db_session.query.return_value.filter.return_value.all.return_value = expected

    assert controller.read_all_for_item(db_session, 5) is expected

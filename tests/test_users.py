from fastapi import HTTPException
import pytest
from controllers import users as controller
from schemas import users as schema


def test_create_user(db_session):
    request = schema.UserCreate(name="Ada Lovelace", email="ada@example.com", role="customer", password="hunter2")

    created_user = controller.create(db_session, request)

    assert created_user is not None
    assert created_user.name == "Ada Lovelace"
    assert created_user.email == "ada@example.com"
    assert created_user.password_hash == "hunter2"
    assert created_user.role == "customer"
    db_session.add.assert_called_once_with(created_user)
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(created_user)


def test_read_all_users(db_session):
    expected = [object(), object()]
    db_session.query.return_value.all.return_value = expected

    assert controller.read_all(db_session) is expected


def test_read_one_user(db_session):
    expected = object()
    db_session.query.return_value.filter.return_value.first.return_value = expected

    assert controller.read_one(db_session, 7) is expected


def test_read_one_user_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        controller.read_one(db_session, 999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Id not found!"


def test_update_user(db_session):
    query = db_session.query.return_value.filter.return_value
    updated = object()
    query.first.side_effect = [object(), updated]
    request = schema.UserUpdate(name="Grace", station="A")

    assert controller.update(db_session, 1, request) is updated
    query.update.assert_called_once_with(
        {"name": "Grace", "station": "A"}, synchronize_session=False
    )
    db_session.commit.assert_called_once()


def test_update_user_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        controller.update(db_session, 999, schema.UserUpdate(name="Nobody"))

    assert exc.value.status_code == 404


def test_delete_user(db_session):
    query = db_session.query.return_value.filter.return_value
    query.first.return_value = object()

    response = controller.delete(db_session, 1)

    assert response.status_code == 204
    query.delete.assert_called_once_with(synchronize_session=False)
    db_session.commit.assert_called_once()


def test_delete_user_not_found(db_session):
    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc:
        controller.delete(db_session, 999)

    assert exc.value.status_code == 404

import pytest
from controllers import users as controller
from schemas import users as schema


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_user(db_session):
    request = schema.UserCreate(name="Ada Lovelace", email="ada@example.com", role="customer", password="hunter2")

    created_user = controller.create(db_session, request)

    assert created_user is not None
    assert created_user.name == "Ada Lovelace"
    assert created_user.email == "ada@example.com"
    assert created_user.password_hash == "hunter2"
    assert created_user.role == "customer"

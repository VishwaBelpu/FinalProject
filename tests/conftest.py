"""Shared test setup.

Importing ``model_loader`` registers every relationship target with SQLAlchemy's
declarative registry.  The unit tests use mocked sessions, so they never connect
to the configured MySQL database.
"""

from models import model_loader  # noqa: F401

import pytest


@pytest.fixture
def db_session(mocker):
    """Return a fresh SQLAlchemy Session-shaped mock."""
    return mocker.Mock()

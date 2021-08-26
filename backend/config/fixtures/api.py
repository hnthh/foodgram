import pytest
from config.testing import ApiClient


@pytest.fixture()
def as_anon():
    return ApiClient()


@pytest.fixture()
def as_user(user):
    return ApiClient(user=user)


@pytest.fixture()
def as_admin(admin):
    return ApiClient(user=admin)

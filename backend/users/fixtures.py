import pytest


@pytest.fixture()
def anon(factory):
    return factory.anon()


@pytest.fixture()
def user(factory):
    return factory.user()


@pytest.fixture()
def admin(factory):
    return factory.user(is_staff=True, is_superuser=True)

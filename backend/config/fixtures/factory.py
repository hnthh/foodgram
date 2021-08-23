import pytest

from config.testing.factory import FixtureFactory


@pytest.fixture()
def factory():
    return FixtureFactory()

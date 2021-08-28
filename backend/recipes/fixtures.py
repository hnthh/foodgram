import pytest


@pytest.fixture()
def recipe(factory):
    return factory.recipe()


@pytest.fixture()
def recipes(factory):
    return factory.recipes()

import pytest
from django.core.management import call_command


@pytest.fixture()
def ingredient(factory):
    return factory.ingredient()


@pytest.fixture()
def ingredients(factory):
    return factory.ingredients()


@pytest.fixture()
def load_ingredients_command_exec():
    return call_command('load_ingredients')

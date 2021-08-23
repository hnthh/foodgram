import pytest

from recipes.models import Ingredient

pytestmark = [pytest.mark.django_db]


def test_db_should_contain_ingredients(load_ingredients_command_exec):
    assert Ingredient.objects.count() == 2191

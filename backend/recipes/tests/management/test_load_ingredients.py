import pytest
from recipes.models import Ingredient

pytestmark = [pytest.mark.django_db]


def test_ok(load_ingredients_command_exec):
    assert Ingredient.objects.count() == 2191


def test_queries_num(django_assert_num_queries):
    from django.core.management import call_command

    with django_assert_num_queries(5):
        call_command('load_ingredients')

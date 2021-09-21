import pytest
from django.core.management import call_command
from ingredients.models import Ingredient

pytestmark = [pytest.mark.django_db]


def test_ok(load_ingredients_command_exec):
    assert Ingredient.objects.count() == 2191

    call_command('load_ingredients')
    assert Ingredient.objects.count() == 2191

    assert Ingredient.objects.filter(
        name='щавель свежий',
        measurement_unit='веточка',
    )
    assert Ingredient.objects.filter(name='молоко 3.6%', measurement_unit='г')
    assert Ingredient.objects.filter(
        name='вишня, протертая с сахаром',
        measurement_unit='г',
    )


def test_queries_num(django_assert_num_queries):
    with django_assert_num_queries(5):
        call_command('load_ingredients')

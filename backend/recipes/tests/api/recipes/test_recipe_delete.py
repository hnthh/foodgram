import pytest
from recipes.models import RecipeIngredient
from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)

    url = f'/api/recipes/{recipe.id}/'

    as_user.delete(url)
    assert not RecipeIngredient.objects.filter(recipe=recipe).exists()


def test_not_found(as_user):
    url = '/api/recipes/1/'
    as_user.delete(url, expected_status=404)


def test_anon(as_anon, recipe):
    as_anon.delete(f'/api/recipes/{recipe.id}/', expected_status=401)

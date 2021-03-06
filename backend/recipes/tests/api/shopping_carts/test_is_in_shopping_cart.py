import pytest
from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)

    recipe_url = f'/api/recipes/{recipe.id}/'
    shopping_cart_url = f'/api/recipes/{recipe.id}/shopping_cart/'

    got = as_user.get(recipe_url)
    assert not got['is_in_shopping_cart']

    as_user.get(shopping_cart_url, expected_status=201)

    got = as_user.get(recipe_url)
    assert got['is_in_shopping_cart']


def test_anon(as_anon, as_user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)
    url = f'/api/recipes/{recipe.id}/'
    got = as_anon.get(url)

    assert not got['is_in_shopping_cart']

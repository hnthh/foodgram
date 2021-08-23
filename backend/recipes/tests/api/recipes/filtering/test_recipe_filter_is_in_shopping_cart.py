import pytest

from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]

URL = '/api/recipes/'


def test_ok(as_user, as_admin, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)
    as_admin.get(f'/api/recipes/{recipe.id}/shopping_cart/', expected_status=201)

    got = as_admin.get(URL)
    assert got['count'] == 2

    got = as_admin.get(URL, {'is_in_shopping_cart': True})
    assert got['count'] == 1


def test_not_found(as_anon):
    got = as_anon.get(URL, {'is_in_shopping_cart': True})

    assert got['count'] == 0

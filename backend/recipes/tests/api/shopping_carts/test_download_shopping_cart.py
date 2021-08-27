import pytest

pytestmark = [pytest.mark.django_db]

URL = '/api/recipes/download_shopping_cart/'


def test_ok(as_user, recipes):
    recipe, another_recipe = recipes

    as_user.get(
        f'/api/recipes/{recipe.id}/shopping_cart/',
        expected_status=201,
    )
    as_user.get(
        f'/api/recipes/{another_recipe.id}/shopping_cart/',
        expected_status=201,
    )
    as_user.get(URL)


def test_anon(as_anon):
    url = '/api/recipes/download_shopping_cart/'
    as_anon.get(url, expected_status=401)

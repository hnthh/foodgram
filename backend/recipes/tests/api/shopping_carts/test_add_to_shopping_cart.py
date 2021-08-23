import pytest

from recipes.models import ShoppingCart
from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]

RESPONSE_FIELDS = (
    'id',
    'name',
    'image',
    'cooking_time',
)


def test_ok(as_user, user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)

    url = f'/api/recipes/{recipe.id}/shopping_cart/'

    got = as_user.get(url, expected_status=201)
    assert ShoppingCart.objects.filter(user=user, recipe=recipe).exists()
    assert tuple(got.keys()) == RESPONSE_FIELDS

    for field in ('id', 'name', 'cooking_time'):
        assert got[field] == getattr(recipe, field)

    assert got['image'].startswith('http://tests')


def test_add_twice(as_user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)

    url = f'/api/recipes/{recipe.id}/shopping_cart/'

    as_user.get(url, expected_status=201)
    got = as_user.get(url, expected_status=400)

    assert got['errors'][0] == 'ShoppingCartObject already exists'


def test_anon(as_anon):
    url = '/api/recipes/1/shopping_cart/'
    as_anon.get(url, expected_status=401)


@pytest.mark.parametrize(
    'method', ['put', 'patch'],
)
def test_method_not_allowed(as_user, method):
    url = '/api/recipes/1/shopping_cart/'
    getattr(as_user, method)(url, expected_status=405)

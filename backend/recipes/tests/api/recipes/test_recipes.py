import pytest

from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]

URL = '/api/recipes/'

PAGINATION_PARAMS = ('count', 'next', 'previous', 'results')

RECIPE_PARAMS = (
    'id',
    'tags',
    'author',
    'ingredients',
    'is_favorited',
    'is_in_shopping_cart',
    'name',
    'image',
    'text',
    'cooking_time',
)


def test_ok(as_anon, as_user, ingredients, tags):
    create_recipes(as_user, ingredients, tags)

    got = as_anon.get(URL)

    assert tuple(got.keys()) == PAGINATION_PARAMS
    assert len(got['results']) == 2
    assert tuple(got['results'][0].keys()) == RECIPE_PARAMS

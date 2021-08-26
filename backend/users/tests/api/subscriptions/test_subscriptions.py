import pytest
from recipes.tests.share import create_recipes
from users.tests.share import create_user_api

pytestmark = [pytest.mark.django_db]

URL = '/api/users/subscriptions/'

RESPONSE_KEYS = (
    'id',
    'email',
    'username',
    'first_name',
    'last_name',
    'is_subscribed',
    'recipes',
    'recipes_count',
)

RECIPE_FIELDS = ('id', 'name', 'image', 'cooking_time')

PAGINATION_PARAMS = ('count', 'next', 'previous', 'results')


def test_ok(as_anon, as_user, as_admin, admin, ingredients, tags):
    another_user = create_user_api(as_anon)
    create_recipes(as_admin, ingredients, tags)

    as_user.get(f'/api/users/{another_user.id}/subscribe/', expected_status=201)
    as_user.get(f'/api/users/{admin.id}/subscribe/', expected_status=201)

    got = as_user.get(URL)

    assert tuple(got.keys()) == PAGINATION_PARAMS
    assert tuple(got['results'][0].keys()) == RESPONSE_KEYS

    assert got['count'] == 2

    results = got['results']
    assert admin.email == results[0]['email']
    assert another_user.email == results[1]['email']

    assert results[0]['is_subscribed']
    assert results[1]['is_subscribed']

    assert len(results[0]['recipes']) == 2
    assert len(results[1]['recipes']) == 0

    assert tuple(results[0]['recipes'][0].keys()) == RECIPE_FIELDS


def test_recipes_limit_recipes_count(as_user, as_admin, admin, ingredients, tags):
    create_recipes(as_admin, ingredients, tags)
    as_user.get(f'/api/users/{admin.id}/subscribe/', expected_status=201)

    got = as_user.get(URL, {'recipes_limit': 1})
    assert len(got['results'][0]['recipes']) == 1
    assert got['results'][0]['recipes_count'] == 2


def test_anon(as_anon):
    as_anon.get(URL, expected_status=401)

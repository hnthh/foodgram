import pytest

from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]

URL = '/api/recipes/'


def test_ok(as_anon, as_user, user, admin, ingredients, tags):
    create_recipes(as_user, ingredients, tags)

    got = as_anon.get(URL, {'author': {user.id}})

    assert got['count'] == 2
    assert got['results'][0]['author']['id'] == user.id
    assert got['results'][1]['author']['id'] == user.id

    got = as_anon.get(URL, {'author': admin.id})

    assert got['count'] == 0


def test_not_found(as_anon):
    as_anon.get(URL, {'author': 1}, expected_status=400)

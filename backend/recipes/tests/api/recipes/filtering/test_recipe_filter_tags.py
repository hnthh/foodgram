import pytest
from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]

URL = '/api/recipes/'


def test_ok(as_anon, as_user, ingredients, tags):
    create_recipes(as_user, ingredients, tags)

    got = as_anon.get(URL, {'tags': 'breakfast'})

    assert got['count'] == 1
    assert got['results'][0]['name'] == 'Лазанья'

    got = as_anon.get(URL, {'tags': 'dinner'})

    assert got['count'] == 1
    assert got['results'][0]['name'] == 'Компот из пряных овощей'

    got = as_anon.get(URL, {'tags': 'lunch'})

    assert got['count'] == 2
    assert got['results'][0]['name'] == 'Компот из пряных овощей'
    assert got['results'][1]['name'] == 'Лазанья'

    got = as_anon.get(URL, {'tags': ('breakfast', 'dinner')})

    assert got['count'] == 2
    assert got['results'][0]['name'] == 'Компот из пряных овощей'
    assert got['results'][1]['name'] == 'Лазанья'


def test_not_found(as_anon):
    as_anon.get(URL, {'tags': 'not-exists'}, expected_status=400)

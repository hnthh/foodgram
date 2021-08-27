import pytest

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, recipe):
    recipe_url = f'/api/recipes/{recipe.id}/'
    favorite_url = f'/api/recipes/{recipe.id}/favorite/'

    got = as_user.get(recipe_url)
    assert not got['is_favorited']

    as_user.get(favorite_url, expected_status=201)

    got = as_user.get(recipe_url)
    assert got['is_favorited']


def test_anon(as_anon, recipe):
    url = f'/api/recipes/{recipe.id}/'
    got = as_anon.get(url)

    assert not got['is_favorited']

import pytest
from recipes.models import Favorite
from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)

    url = f'/api/recipes/{recipe.id}/favorite/'

    as_user.get(url, expected_status=201)
    assert Favorite.objects.filter(user=user, recipe=recipe).exists()

    as_user.delete(url)
    assert not Favorite.objects.filter(user=user, recipe=recipe).exists()


def test_not_found(as_user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)

    url = f'/api/recipes/{recipe.id}/favorite/'
    got = as_user.delete(url, expected_status=400)
    assert got['errors'] == 'FavoriteObject does not exist'


def test_anon(as_anon):
    url = '/api/recipes/1/favorite/'
    as_anon.delete(url, expected_status=401)

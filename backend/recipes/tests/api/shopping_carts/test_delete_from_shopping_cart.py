import pytest
from recipes.models import ShoppingCart

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, user, recipe):
    url = f'/api/recipes/{recipe.id}/shopping_cart/'

    as_user.get(url, expected_status=201)
    assert ShoppingCart.objects.filter(user=user, recipe=recipe).exists()

    as_user.delete(url)
    assert not ShoppingCart.objects.filter(user=user, recipe=recipe).exists()


def test_not_found(as_user, recipe):
    url = f'/api/recipes/{recipe.id}/shopping_cart/'
    got = as_user.delete(url, expected_status=400)
    assert got['errors'] == 'ShoppingCartObject does not exist'


def test_anon(as_anon):
    url = '/api/recipes/1/shopping_cart/'
    as_anon.delete(url, expected_status=401)

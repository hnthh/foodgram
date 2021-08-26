import pytest
from recipes.models import Recipe
from recipes.tests.share import create_recipes
from users.models import Subscribe

pytestmark = [pytest.mark.django_db]

FIELDS = (
    'id',
    'email',
    'username',
    'first_name',
    'last_name',
)


def test_ok(as_admin, admin, as_user, user, ingredients, tags):
    create_recipes(as_admin, ingredients, tags)

    url = f'/api/users/{admin.id}/subscribe/'

    got = as_user.get(url, expected_status=201)
    assert Subscribe.objects.filter(user=user, author=admin).exists()

    response_keys = FIELDS + ('is_subscribed', 'recipes', 'recipes_count')
    assert tuple(got.keys()) == response_keys

    for field in FIELDS:
        assert got[field] == getattr(admin, field)

    assert got['is_subscribed']
    assert len(got['recipes']) == got['recipes_count'] == 2
    assert tuple(got['recipes'][0]) == ('id', 'name', 'image', 'cooking_time')
    assert Recipe.objects.get(id=got['recipes'][0]['id']).author == admin


def test_self_subscribe(as_user, user):
    url = f'/api/users/{user.id}/subscribe/'
    got = as_user.get(url, expected_status=400)
    assert not Subscribe.objects.filter(user=user, author=user).exists()
    assert (
        'You cannot subscribe/unsubscribe to yourself'
        in got['errors']
    )


def test_subscribe_twice(as_user, user, admin):
    url = f'/api/users/{admin.id}/subscribe/'
    as_user.get(url, expected_status=201)
    assert Subscribe.objects.filter(user=user, author=admin).exists()

    got = as_user.get(url, expected_status=400)
    assert (
        'Subscribe object with given credentials already exists'
        in got['errors']
    )


def test_anon(as_anon, user):
    url = f'/api/users/{user.id}/subscribe/'
    as_anon.get(url, expected_status=401)

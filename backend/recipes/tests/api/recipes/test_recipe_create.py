import pytest

pytestmark = [pytest.mark.django_db]

URL = '/api/recipes/'


def test_ok(as_user, user, ingredients, tags):
    ingredient, another_ingredient = ingredients
    tag, another_tag, _ = tags

    data = {
        'name': 'Лазанья',
        'text': 'То, что Гарфилд любит!',
        'cooking_time': 30,
        'ingredients': [
            {'id': ingredient.id, 'amount': 43},
            {'id': another_ingredient.id, 'amount': 76},
        ],
        'tags': [tag.pk, another_tag.pk],
        'image': (
            'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
        ),
    }

    got = as_user.post(URL, data, format='json')

    assert len(got) == 10
    assert got['id'] == 1
    assert got['tags'] == [
        {'id': tag.pk, 'name': tag.name, 'color': tag.color, 'slug': tag.slug},
        {
            'id': another_tag.pk,
            'name': another_tag.name,
            'color': another_tag.color,
            'slug': another_tag.slug,
        },
    ]
    assert got['author'] == {
        'id': 1,
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_subscribed': False,
    }
    assert got['ingredients'] == [
        {
            'id': 1,
            'name': ingredient.name,
            'measurement_unit': ingredient.measurement_unit,
            'amount': 43,
        },
        {
            'id': 2,
            'name': another_ingredient.name,
            'measurement_unit': another_ingredient.measurement_unit,
            'amount': 76,
        },
    ]
    assert got['name'] == data['name']
    assert got['text'] == data['text']
    assert got['cooking_time'] == data['cooking_time']
    assert got['image'].startswith('http://tests')
    assert not got['is_favorited']
    assert not got['is_in_shopping_cart']


def test_anon(as_anon):
    as_anon.post(URL, expected_status=401)

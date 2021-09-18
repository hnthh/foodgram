import pytest
from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)

    url = f'/api/recipes/{recipe.id}/'
    ingredient, another_ingredient = ingredients
    tag, *_ = tags

    data = {
        'name': 'Лазанья Modified',
        'text': 'То, что Гарфилд любит!',
        'cooking_time': 70,
        'ingredients': [
            {'id': ingredient.id, 'amount': 30},
            {'id': another_ingredient.id, 'amount': 40},
        ],
        'tags': [tag.pk],
        'image': 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
    }

    got = as_user.put(url, data, format='json')

    assert not got['is_favorited']
    assert got['name'] == data['name']
    assert got['text'] == data['text']
    assert got['cooking_time'] == data['cooking_time']
    assert got['ingredients'] == [
        {
            'id': 1,
            'name': ingredient.name,
            'measurement_unit': ingredient.measurement_unit,
            'amount': 30,
        },
        {
            'id': 2,
            'name': another_ingredient.name,
            'measurement_unit': another_ingredient.measurement_unit,
            'amount': 40,
        },
    ]
    assert got['tags'] == [
        {'id': tag.pk, 'name': tag.name, 'color': tag.color, 'slug': tag.slug},
    ]
    assert got['image'].startswith('http://tests')


def test_anon(as_anon, recipe):
    as_anon.put(f'/api/recipes/{recipe.id}/', expected_status=401)


def test_patch(as_user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)

    url = f'/api/recipes/{recipe.id}/'

    ingredient, another_ingredient = ingredients
    tag, *_ = tags

    data = {
        'ingredients': [
            {'id': ingredient.id, 'amount': 30},
            {'id': another_ingredient.id, 'amount': 40},
        ],
        'tags': [tag.pk],
    }

    got = as_user.patch(url, data, format='json')

    assert not got['is_favorited']
    assert got['name'] == recipe.name
    assert got['text'] == recipe.text
    assert got['cooking_time'] == recipe.cooking_time
    assert got['ingredients'] == [
        {
            'id': 1,
            'name': ingredient.name,
            'measurement_unit': ingredient.measurement_unit,
            'amount': 30,
        },
        {
            'id': 2,
            'name': another_ingredient.name,
            'measurement_unit': another_ingredient.measurement_unit,
            'amount': 40,
        },
    ]
    assert got['tags'] == [
        {'id': tag.pk, 'name': tag.name, 'color': tag.color, 'slug': tag.slug},
    ]
    assert got['image'].split('/')[-1] == recipe.image.url.split('/')[-1]

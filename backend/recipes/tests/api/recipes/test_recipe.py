import pytest
from recipes.tests.share import create_recipes

pytestmark = [pytest.mark.django_db]


def test_ok(as_anon, as_user, user, ingredients, tags):
    recipe, _ = create_recipes(as_user, ingredients, tags)
    ingredient, another_ingredient = ingredients
    tag, another_tag, _ = tags

    url = f'/api/recipes/{recipe.id}/'

    got = as_anon.get(url)

    assert len(got) == 10
    assert got['id'] == recipe.id
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
    assert got['name'] == got['name']
    assert got['text'] == got['text']
    assert got['cooking_time'] == got['cooking_time']
    assert got['image'].startswith('http://tests')
    assert not got['is_favorited']
    assert not got['is_in_shopping_cart']

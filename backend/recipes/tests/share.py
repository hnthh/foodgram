from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()


def create_recipes(client, ingredients, tags):
    def create_recipe(name, text, cooking_time, ingredients, tags):
        data = {
            'name': name,
            'text': text,
            'cooking_time': cooking_time,
            'ingredients': ingredients,
            'tags': tags,
            'image': 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==',
        }
        client.post('/api/recipes/', data=data, format='json')
        return Recipe.objects.latest('pk')

    result = list()
    result.append(
        create_recipe(
            name='Лазанья',
            text='То, что Гарфилд любит!',
            cooking_time=60,
            ingredients=[{'id': 1, 'amount': 43}, {'id': 2, 'amount': 76}],
            tags=[1, 2],
        ),
    )
    result.append(
        create_recipe(
            name='Компот из пряных овощей',
            text='Вам не послышалось.',
            cooking_time=68,
            ingredients=[{'id': 1, 'amount': 34}, {'id': 2, 'amount': 67}],
            tags=[2, 3],
        ),
    )
    return result

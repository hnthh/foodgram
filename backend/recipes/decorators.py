from recipes.models import Ingredient, RecipeIngredient
from rest_framework.generics import get_object_or_404


def recipe_create_update(func):
    def wrapper(*args):
        ingredients = args[-1].pop('ingredients')
        tags = args[-1].pop('tags')

        recipe = func(*args)

        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                amount=ingredient['amount'],
            )
        recipe.tags.set(tags)
        return recipe
    return wrapper


def recipe_filter_bool_param(func):
    def wrapper(*args):
        self, qs, _, value = args
        user = self.request.user

        if value and user.is_authenticated:
            qs = func(*args)
        return qs
    return wrapper

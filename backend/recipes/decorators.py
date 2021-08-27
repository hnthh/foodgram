from functools import wraps

from django.core.exceptions import ObjectDoesNotExist
from recipes.models import Ingredient, RecipeIngredient
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response


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


def recipe_favorite_shoppingcart_actions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self, request = args
        pk = kwargs['pk']

        user = request.user
        model_name = self.serializer_class.Meta.model.__name__

        if request.method == 'DELETE':
            try:
                func(*args, **kwargs)
            except ObjectDoesNotExist:
                return Response(
                    {'errors': f'{model_name}Object does not exist'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = {'user': user.pk, 'recipe': pk}
        serializer = self.get_serializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return wrapper


def recipe_filter_bool_param(func):
    def wrapper(*args):
        self, qs, _, value = args
        user = self.request.user

        if value and user.is_authenticated:
            qs = func(*args)
        return qs
    return wrapper

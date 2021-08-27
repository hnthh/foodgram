import pytest
from django.core.exceptions import ValidationError
from recipes.models import RecipeIngredient

pytestmark = [pytest.mark.django_db]


def test_gt(recipe, ingredient):

    with pytest.raises(
        ValidationError,
        match='Ensure this value is greater than 0.',
    ):
        RecipeIngredient.objects.create(
            ingredient=ingredient,
            recipe=recipe,
            amount=0,
        )


def test_lt(recipe, ingredient):

    with pytest.raises(
        ValidationError,
        match="That's too much, man!",
    ):
        RecipeIngredient.objects.create(
            ingredient=ingredient,
            recipe=recipe,
            amount=5001,
        )

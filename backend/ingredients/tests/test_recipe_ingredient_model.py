import pytest
from django.db.utils import IntegrityError
from ingredients.models import RecipeIngredient

pytestmark = [pytest.mark.django_db]


def test_amount_gt(recipe, ingredient):

    with pytest.raises(
        IntegrityError,
        match='CHECK constraint failed: amount_gt_0',
    ):
        RecipeIngredient.objects.create(
            ingredient=ingredient,
            recipe=recipe,
            amount=0,
        )


def test_amount_lt(recipe, ingredient):

    with pytest.raises(
        IntegrityError,
        match='CHECK constraint failed: amount_lt_5000',
    ):
        RecipeIngredient.objects.create(
            ingredient=ingredient,
            recipe=recipe,
            amount=5001,
        )

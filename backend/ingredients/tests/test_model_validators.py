import pytest
from django.db.utils import IntegrityError
from ingredients.models import Ingredient

pytestmark = [pytest.mark.django_db]


@pytest.mark.xfail(reason='Wrong message')
def test_unique_ingredient_unit_constraint(ingredient):

    with pytest.raises(
        IntegrityError,
        match='UNIQUE constraint failed: unique_ingredient_unit',
    ):
        Ingredient.objects.create(
            name=ingredient.name,
            measurement_unit=ingredient.measurement_unit,
        )

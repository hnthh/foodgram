import pytest
from django.db.utils import IntegrityError
from recipes.models import Tag

pytestmark = [pytest.mark.django_db]


def test_invalid_color():
    color = 'invalid-color'

    with pytest.raises(
        IntegrityError,
        match='CHECK constraint failed: HEX_color',
    ):
        Tag.objects.create(
            name='Полдник',
            color=color,
            slug='afternoon-tea',
        )

import pytest
from django.core.exceptions import ValidationError
from recipes.models import Tag

pytestmark = [pytest.mark.django_db]


def test_invalid_color():
    color = 'invalid-color'

    with pytest.raises(
        ValidationError,
        match=f'{color} is not a HEX color code.',
    ):
        Tag.objects.create(
            name='Полдник',
            color=color,
            slug='afternoon-tea',
        )

import pytest

pytestmark = [pytest.mark.django_db]

RESPONSE_FIELDS = (
    'id',
    'name',
    'measurement_unit',
)


def test_ok(as_anon, ingredient):
    url = f'/api/ingredients/{ingredient.id}/'
    got = as_anon.get(url)

    for field in RESPONSE_FIELDS:
        assert got[field] == getattr(ingredient, field)

import pytest

pytestmark = [pytest.mark.django_db]

URL = '/api/ingredients/'

RESPONSE_FIELDS = (
    'id',
    'name',
    'measurement_unit',
)


def test_ok(as_anon, ingredients):
    got = as_anon.get(URL)

    ingredient, _ = ingredients

    for field in RESPONSE_FIELDS:
        assert got[0][field] == getattr(ingredient, field)


def test_filter_by_name(
    as_anon,
    load_ingredients_command_exec,
):
    got = as_anon.get(URL, {'search': {'абри'}})

    assert len(got)
    assert got[4]['name'].startswith('абри')


def test_method_not_allowed(as_user):
    as_user.post('/api/users/me/', expected_status=405)

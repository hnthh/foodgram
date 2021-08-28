import pytest

pytestmark = [pytest.mark.django_db]

URL = '/api/tags/'

RESPONSE_FIELDS = (
    'id',
    'name',
    'color',
    'slug',
)


def test_ok(as_anon, tags):
    got = as_anon.get(URL)

    tag, *_ = tags
    assert len(got) == 3

    for field in RESPONSE_FIELDS:
        assert got[0][field] == getattr(tag, field)


def test_method_not_allowed(as_user):
    as_user.post(URL, expected_status=405)

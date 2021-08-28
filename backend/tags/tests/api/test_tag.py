import pytest

pytestmark = [pytest.mark.django_db]

RESPONSE_FIELDS = (
    'id',
    'name',
    'color',
    'slug',
)


def test_ok(as_anon, tag):
    url = f'/api/tags/{tag.id}/'
    got = as_anon.get(url)

    for field in RESPONSE_FIELDS:
        assert got[field] == getattr(tag, field)


def test_not_found(as_user):
    url = '/api/tags/1/'
    as_user.get(url, expected_status=404)


def test_method_not_allowed(as_user, tag):
    url = f'/api/tags/{tag.id}/'
    as_user.post(url, expected_status=405)

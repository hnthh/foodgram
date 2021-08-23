import pytest

pytestmark = [pytest.mark.django_db]

RESPONSE_FIELDS = (
    'id',
    'email',
    'username',
    'first_name',
    'last_name',
)


def test_ok(as_user, admin):
    url = f'/api/users/{admin.id}/'
    got = as_user.get(url)

    for field in RESPONSE_FIELDS:
        assert got[field] == getattr(admin, field)

    assert not got['is_subscribed']


def test_anon(as_anon, admin):
    url = f'/api/users/{admin.id}/'
    as_anon.get(url, expected_status=401)

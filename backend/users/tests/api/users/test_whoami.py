import pytest

pytestmark = [pytest.mark.django_db]

URL = '/api/users/me/'

FIELDS = (
    'id',
    'email',
    'username',
    'first_name',
    'last_name',
)


def test_ok(as_user, user):
    got = as_user.get(URL)

    assert len(got) == 6

    for field in FIELDS:
        assert got[field] == getattr(user, field)

    assert not got['is_subscribed']


def test_anon(as_anon):
    as_anon.get(URL, expected_status=401)


@pytest.mark.parametrize(
    'method', ['put', 'patch', 'delete'],
)
def test_method_not_allowed(as_user, method):
    getattr(as_user, method)(URL, expected_status=405)

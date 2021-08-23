import pytest

pytestmark = [pytest.mark.django_db]

URL = '/api/users/'

RESPONSE_FIELDS = (
    'id',
    'email',
    'username',
    'first_name',
    'last_name',
)

PAGINATION_PARAMS = ('count', 'next', 'previous', 'results')


def test_ok(as_anon, user, admin):
    got = as_anon.get(URL)

    assert tuple(got.keys()) == PAGINATION_PARAMS
    assert got['count'] == 2

    for field in RESPONSE_FIELDS:
        assert got['results'][0][field] == getattr(user, field)
    assert got['results'][1]['email'] == admin.email

    assert not got['results'][0]['is_subscribed']

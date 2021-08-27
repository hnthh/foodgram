import pytest

pytestmark = [pytest.mark.django_db]


def test_ok(as_user, admin):
    url = f'/api/users/{admin.id}/'

    got = as_user.get(url)
    assert got['email'] == admin.email
    assert not got['is_subscribed']

    as_user.get(f'/api/users/{admin.id}/subscribe/', expected_status=201)

    got = as_user.get(url)
    assert got['is_subscribed']

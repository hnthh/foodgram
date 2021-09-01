import pytest
from users.models import Subscribe

pytestmark = [pytest.mark.django_db]


def test_ok(admin, as_user, user):
    as_user.get(
        f'/api/users/{admin.id}/subscribe/',
        expected_status=201,
    )
    assert Subscribe.objects.filter(user=user, author=admin).exists()

    as_user.delete(
        f'/api/users/{admin.id}/subscribe/',
        expected_status=204,
    )
    assert not Subscribe.objects.filter(user=user, author=admin).exists()


def test_not_exists(as_user, admin):
    url = f'/api/users/{admin.id}/subscribe/'

    got = as_user.delete(url, expected_status=400)
    assert 'Subscription does not exist' in got['errors']


def test_anon(as_anon, user):
    url = f'/api/users/{user.id}/subscribe/'
    as_anon.delete(url, expected_status=401)

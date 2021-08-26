import pytest
from users.tests.share import auth_client, create_user_api

pytestmark = [pytest.mark.django_db]

URL = '/api/users/set_password/'


def test_ok(as_anon):
    user = create_user_api(as_anon)
    as_user = auth_client(user)

    data = {
        'new_password': 'oweihrjg38391#',
        'current_password': 'wert1234gsa$',
    }
    as_user.post(URL, data, expected_status=204)

    user.refresh_from_db()
    assert user.check_password(data['new_password'])


def test_anon(as_anon):
    as_anon.get(URL, expected_status=401)

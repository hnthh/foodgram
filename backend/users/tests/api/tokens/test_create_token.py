import pytest
from rest_framework.authtoken.models import Token
from users.tests.share import create_user_api

pytestmark = [pytest.mark.django_db]

URL = '/api/auth/token/login/'


def test_ok(as_anon):
    user = create_user_api(as_anon)

    data = {
        'email': user.email,
        'password': 'wert1234gsa$',
    }
    got = as_anon.post(URL, data, expected_status=200)
    assert Token.objects.filter(user=user).exists()
    assert 'auth_token' in got

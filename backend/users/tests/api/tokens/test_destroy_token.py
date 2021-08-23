import pytest
from rest_framework.authtoken.models import Token

pytestmark = [pytest.mark.django_db]

URL = '/api/auth/token/logout/'


def test_ok(as_user, user):
    assert Token.objects.filter(user=user).exists()

    as_user.post(URL, expected_status=204)
    assert not Token.objects.filter(user=user).exists()

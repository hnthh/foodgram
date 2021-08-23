from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()

USER_CREATE_DATA = {
    'email': 'testuser@test.com',
    'username': 'TestUser',
    'first_name': 'Test',
    'last_name': 'User',
    'password': 'wert1234gsa$',
}


def create_user_api(client) -> User:
    client.post('/api/users/', data=USER_CREATE_DATA)
    return User.objects.get(username=USER_CREATE_DATA['username'])


def auth_client(user):
    token = Token.objects.create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    return client

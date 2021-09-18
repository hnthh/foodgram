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


def test_ok(as_anon, django_user_model):
    got = as_anon.post(
        URL,
        {
            'email': 'testuser@test.com',
            'username': 'TestUser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'wert1234gsa$',
        },
    )

    assert tuple(got.keys()) == RESPONSE_FIELDS
    created = django_user_model.objects.get(id=got['id'])

    for field in RESPONSE_FIELDS:
        assert got[field] == getattr(created, field)

    assert created.check_password('wert1234gsa$')


def test_invalid_payload(as_anon, user):
    as_anon.post(URL, {}, expected_status=400)

    as_anon.post(
        URL,
        {'email': 'testuser@test.com', 'username': 'TestUser', 'password': 'wert1234gsa$'},
        expected_status=400,
    )

    got = as_anon.post(
        URL,
        {
            'email': user.email,
            'username': 'TestUser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'wert1234gsa$',
        },
        expected_status=400,
    )
    assert got['email'][0] == 'Пользователь с такой почтой уже зарегистрирован на платформе.'

    got = as_anon.post(
        URL,
        {
            'email': 'testuser@test.com',
            'username': user.username,
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'wert1234gsa$',
        },
        expected_status=400,
    )
    assert got['username'][0] == 'Пользователь с таким логином уже зарегистрирован на платформе.'

    got = as_anon.post(
        URL,
        {
            'email': 'testuser@test.com',
            'username': '!',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'wert1234gsa$',
        },
        expected_status=400,
    )
    assert got['username'][0] == (
        'Введите правильный логин. '
        'Он может содержать только буквы, цифры и знаки @/./+/-/_.'
    )

from users.models import Subscribe


class Subscriber:
    def __init__(self, user, author):
        self._user = user
        self._author = author

    def __call__(self, *args, **kwargs):
        return self._factory()

    def _factory(self):
        return Subscribe.objects.create(
            user=self._user,
            author=self._author,
        )

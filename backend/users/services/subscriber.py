from users.models import Subscribe


class Subscriber:
    def __init__(self, user, author):
        self.user = user
        self.author = author

    def __call__(self, *args, **kwargs):
        self.subscribe()

    def subscribe(self):
        Subscribe.objects.create(user=self.user, author=self.author)

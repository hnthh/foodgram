from users.models import Subscribe


class Unsubscriber:
    def __init__(self, user, author):
        self.user = user
        self.author = author

    def __call__(self, *args, **kwargs):
        self.unsubscribe()

    def unsubscribe(self):
        Subscribe.objects.get(user=self.user, author=self.author).delete()

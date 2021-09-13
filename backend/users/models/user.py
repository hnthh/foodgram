from config.models import DefaultUserQuerySet, models
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Exists, OuterRef, Q, Value


class UserQuerySet(DefaultUserQuerySet):

    class Q:  # noqa: PIE798
        @staticmethod
        def user_following(user):
            return Q(following__user=user)

    def for_detail(self, pk, user):
        return self.for_viewset(user).get(id=pk)

    def for_anon(self):
        return self.annotate(
            is_subscribed=Value(False),
            recipes_count=Value(0),
        )

    def for_viewset(self, user):
        from users.models import Subscribe

        if not user.is_authenticated:
            return self.for_anon()

        return self.annotate(
            is_subscribed=Exists(Subscribe.objects.filter(user=user, author=OuterRef('pk'))),
            recipes_count=Count('recipes'),
        )

    def for_subscriptions(self, user):
        qs = self.for_viewset(user)

        if not user.is_authenticated:
            return self.for_anon()

        return qs.filter(self.Q.user_following(user))


class User(AbstractUser):
    objects = UserQuerySet.as_manager()

    username_validator = AbstractUser.username_validator

    username = models.CharField('логин', unique=True, max_length=150, validators=[username_validator])
    email = models.EmailField('почта', unique=True, max_length=150)
    first_name = models.CharField('имя', max_length=150)
    last_name = models.CharField('фамилия', max_length=150)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        swappable = 'AUTH_USER_MODEL'
        constraints = (
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_email_username',
            ),
        )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def subscribe(self, to):
        from users.services import Subscriber
        return Subscriber(self, to)()

    def unsubscribe(self, fromm):
        from users.services import Unsubscriber
        return Unsubscriber(self, fromm)()

from config.models import DefaultUserQuerySet, models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class UserQuerySet(DefaultUserQuerySet):

    class Q:  # noqa: PIE798
        @staticmethod
        def user_following(user):
            return Q(following__user=user)

    def for_subscriptions(self, user):
        if not user.is_authenticated:
            return self

        return self.filter(self.Q.user_following(user))


class User(AbstractUser):
    objects = UserQuerySet.as_manager()

    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        constraints = (
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_email_username',
            ),
        )

    def __str__(self):
        name = f'{self.first_name} {self.last_name}'

        if len(name) < 3:
            return _('Anonymous')

        return name.strip()

    def subscribe(self, to):
        from users.services import Subscriber
        return Subscriber(self, to)()

    def unsubscribe(self, fromm):
        from users.services import Unsubscriber
        return Unsubscriber(self, fromm)()

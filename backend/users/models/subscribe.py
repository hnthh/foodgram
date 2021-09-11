from config.models import TimestampedModel, models
from django.db.models import F
from django.utils.translation import gettext_lazy as _


class Subscribe(TimestampedModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='followers')
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        constraints = (
            models.CheckConstraint(name='user_not_author', check=~models.Q(user=F('author'))),
            models.UniqueConstraint(fields=('user', 'author'), name='unique_user_author'),
        )

    def __str__(self):
        return f'{self.user} / {self.author}'

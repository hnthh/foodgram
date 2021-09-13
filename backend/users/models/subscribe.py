from config.models import TimestampedModel, models
from django.db.models import F


class Subscribe(TimestampedModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='подписчик',
    )
    author = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор',
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = (
            models.CheckConstraint(name='user_not_author', check=~models.Q(user=F('author'))),
            models.UniqueConstraint(fields=('user', 'author'), name='unique_user_author'),
        )

    def __str__(self):
        return f'{self.user} / {self.author}'

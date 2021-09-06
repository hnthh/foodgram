from config.models import TimestampedModel, models
from django.db.models import F


class Subscribe(TimestampedModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='followers')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = (
            models.CheckConstraint(name='user_not_author', check=~models.Q(user=F('author'))),
            models.UniqueConstraint(fields=('user', 'author'), name='unique_user_author'),
        )

    def __str__(self):
        return f'{self.user} / {self.author}'

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F

User = get_user_model()


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                name='user_not_author',
                check=~models.Q(user=F('author')),
            ),
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_author',
            ),
        )

    def __str__(self):
        return f'{self.user} / {self.author}'

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

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
        return self.username


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

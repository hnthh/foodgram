from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

User = get_user_model()

HEX_RE = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex=HEX_RE,
                message='%(value)s is not a HEX color code.',
            ),
        ],
    )
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                name='HEX_color',
                check=models.Q(color__regex=HEX_RE),
            ),
        )

    def __str__(self):
        return self.name

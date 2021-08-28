from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='purchases',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} / {self.recipe}'

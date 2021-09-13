from config.models import TimestampedModel, models


class ShoppingCart(TimestampedModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь')
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, verbose_name='рецепт')

    class Meta:
        verbose_name = 'покупка'
        verbose_name_plural = 'покупки'
        default_related_name = 'purchases'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_purchase_user_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} / {self.recipe}'

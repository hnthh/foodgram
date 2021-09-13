from config.models import TimestampedModel, models


class Favorite(TimestampedModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='пользователь')
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE, verbose_name='рецепт')

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранное'
        default_related_name = 'favourites'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} / {self.recipe}'

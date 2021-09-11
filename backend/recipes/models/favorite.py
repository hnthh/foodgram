from config.models import DefaultModel, models
from django.utils.translation import gettext_lazy as _


class Favorite(DefaultModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    recipe = models.ForeignKey('recipes.Recipe', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('favourites')
        verbose_name_plural = _('favourites')
        default_related_name = 'favourites'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_user_recipe',
            ),
        )

    def __str__(self):
        return f'{self.user} / {self.recipe}'

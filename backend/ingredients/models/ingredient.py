from config.models import DefaultModel, models
from django.utils.translation import gettext_lazy as _


class Ingredient(DefaultModel):
    name = models.CharField(_('name'), max_length=128)
    measurement_unit = models.CharField(_('measurement unit'), max_length=64)

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient_measurementunit',
            ),
        )

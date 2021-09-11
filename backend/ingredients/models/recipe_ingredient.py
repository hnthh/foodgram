from config.models import DefaultModel, models
from config.validators import GteMinValueValidator
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _


class RecipeIngredient(DefaultModel):
    ingredient = models.ForeignKey(
        'ingredients.Ingredient',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        _('amount'),
        decimal_places=1,
        max_digits=5,
        validators=[
            GteMinValueValidator(0),
            MaxValueValidator(5000, _("That's too much, man!")),
        ],
    )

    class Meta:
        verbose_name = _('recipe ingredient')
        verbose_name_plural = _('recipe ingredients')
        default_related_name = 'recipeingredients'
        constraints = (
            models.CheckConstraint(name='amount_gt_0', check=models.Q(amount__gt=0)),
            models.CheckConstraint(name='amount_lt_5000', check=models.Q(amount__lt=5000)),
            models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_recipe_ingredient'),
        )

    def __str__(self):
        return f'{self.amount} / {self.ingredient}'

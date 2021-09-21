from config.models import DefaultModel, models
from config.validators import GteMinValueValidator
from django.core.validators import MaxValueValidator


class RecipeIngredient(DefaultModel):
    ingredient = models.ForeignKey(
        'ingredients.Ingredient',
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    amount = models.DecimalField(
        'количество',
        decimal_places=1,
        max_digits=5,
        validators=[
            GteMinValueValidator(
                0,
                'Введите число больше нуля или удалите ингредиент.',
            ),
            MaxValueValidator(5000, 'Это ну оооочень много!'),
        ],
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        default_related_name = 'recipeingredients'
        constraints = (
            models.CheckConstraint(
                name='amount_gt_0',
                check=models.Q(amount__gt=0),
            ),
            models.CheckConstraint(
                name='amount_lt_5000',
                check=models.Q(amount__lt=5000),
            ),
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient',
            ),
        )

    def __str__(self):
        return f'{self.amount} / {self.ingredient}'

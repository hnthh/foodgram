from config.validators import GtMinValueValidator
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from ingredients.models import Ingredient

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


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(max_length=256)
    text = models.TextField()
    image = models.ImageField(upload_to='recipes/images/')
    cooking_time = models.PositiveSmallIntegerField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        blank=True,
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_author_recipename',
            ),
        )
        ordering = ('-created',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=1,
        max_digits=5,
        validators=[
            GtMinValueValidator(0),
            MaxValueValidator(5000, _("That's too much, man!")),
        ],
    )

    class Meta:
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


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
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


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases',
    )
    recipe = models.ForeignKey(
        Recipe,
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

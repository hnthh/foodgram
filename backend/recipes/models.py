from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


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
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='%(value)s is not a HEX color code.',
            ),
        ],
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    measurement_unit = models.CharField(max_length=64)

    class Meta:
        unique_together = ('name', 'measurement_unit')

    def __str__(self):
        return f'{self.name}'


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
        unique_together = ('author', 'name')
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
            MinValueValidator(0.1),
        ],
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')

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
        unique_together = ('user', 'recipe')

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
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f'{self.user} / {self.recipe}'

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
        'ingredients.Ingredient',
        through='ingredients.RecipeIngredient',
        related_name='recipes',
        blank=True,
    )
    tags = models.ManyToManyField(
        'tags.Tag',
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

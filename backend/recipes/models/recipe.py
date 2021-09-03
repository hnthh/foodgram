from config.models import DefaultQuerySet, TimestampedModel, models


class RecipeQuerySet(DefaultQuerySet):
    pass


class Recipe(TimestampedModel):
    objects: RecipeQuerySet = RecipeQuerySet.as_manager()

    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='recipes')
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
    tags = models.ManyToManyField('tags.Tag', related_name='recipes', blank=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'name'),
                name='unique_author_recipename',
            ),
        )
        ordering = ('-created', '-modified')

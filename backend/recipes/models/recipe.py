from config.models import DefaultQuerySet, TimestampedModel, models
from django.db.models import Exists, OuterRef, Value


class RecipeQuerySet(DefaultQuerySet):

    def for_detail(self, pk, user):
        return self.for_viewset(user).get(id=pk)

    def for_viewset(self, user):
        from recipes.models import Favorite, ShoppingCart

        if not user.is_authenticated:
            return self.annotate(
                is_favorited=Value(False),
                is_in_shopping_cart=Value(False),
            )

        return self.annotate(
            is_favorited=Exists(Favorite.objects.filter(recipe=OuterRef('pk'), user=user)),
            is_in_shopping_cart=Exists(ShoppingCart.objects.filter(recipe=OuterRef('pk'), user=user)),
        )


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
            models.UniqueConstraint(fields=('author', 'name'), name='unique_author_recipename'),
        )
        ordering = ('-created', '-modified')

from config.models import DefaultQuerySet, TimestampedModel, models
from django.db.models import Exists, OuterRef, Q, Value
from django.utils.translation import gettext_lazy as _


class RecipeQuerySet(DefaultQuerySet):

    class Q:  # noqa: PIE798
        @staticmethod
        def author(user):
            return Q(author=user)

    def for_detail(self, pk, user):
        return self.for_viewset(user).get(id=pk)

    def for_anon(self):
        return self.annotate(
            is_favorited=Value(False),
            is_in_shopping_cart=Value(False),
        )

    def for_viewset(self, user):
        from recipes.models import Favorite, ShoppingCart

        if not user.is_authenticated:
            return self.for_anon()

        return self.annotate(
            is_favorited=Exists(Favorite.objects.filter(recipe=OuterRef('pk'), user=user)),
            is_in_shopping_cart=Exists(ShoppingCart.objects.filter(recipe=OuterRef('pk'), user=user)),
        )

    def for_author(self, user):
        qs = self.for_viewset(user)

        if not user.is_authenticated:
            return self.for_anon()

        return qs.filter(self.Q.author(user))

    def create_with_ingredients_and_tags(self, **data):
        from recipes.services import RecipeCreator
        return RecipeCreator(**data)()


class Recipe(TimestampedModel):
    objects = RecipeQuerySet.as_manager()

    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name = models.CharField(_('recipe name'), max_length=256)
    text = models.TextField(_('recipe description'))
    image = models.ImageField(_('image'), upload_to='recipes/images/')
    cooking_time = models.PositiveSmallIntegerField(_('cooking time'))
    ingredients = models.ManyToManyField(
        'ingredients.Ingredient',
        through='ingredients.RecipeIngredient',
        blank=True,
    )
    tags = models.ManyToManyField('tags.Tag', blank=True)

    class Meta:
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')
        default_related_name = 'recipes'
        constraints = (
            models.UniqueConstraint(fields=('author', 'name'), name='unique_author_recipename'),
        )
        ordering = ('-created', '-modified')

    def update(self, **data):
        from recipes.services import RecipeUpdater
        return RecipeUpdater(self, **data)()

import django_filters as filters

from recipes.decorators import recipe_filter_bool_param
from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
        )

    @recipe_filter_bool_param
    def filter_is_favorited(self, queryset, name, value):
        return queryset.filter(
            favorite__user=self.request.user,
        )

    @recipe_filter_bool_param
    def filter_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(
            purchases__user=self.request.user,
        )


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)

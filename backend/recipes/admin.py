from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from ingredients.models import RecipeIngredient
from recipes.models import Favorite, Recipe, ShoppingCart


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (
        RecipeIngredientInline,
    )
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    list_display = (
        'author',
        'name',
        'created',
        'count_favorite',
    )

    def count_favorite(self, recipe):
        return Favorite.objects.filter(
            recipe=recipe,
        ).count()


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass

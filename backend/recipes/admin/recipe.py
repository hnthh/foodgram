from config.admin import AppAdmin, admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from recipes.models import Recipe, RecipeIngredient


class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(AppAdmin):
    inlines = (
        RecipeIngredientInline,
    )
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    list_display = (
        'name',
        'author',
        'count_favorites',
    )
    list_filter = (
        'tags',
    )
    fields = (
        'author',
        'name',
        'text',
        'image',
        'cooking_time',
        'tags',
    )

    def get_ordering(self, request):
        return ['-favourites']

    @admin.display(description='добавлений в избранное')
    def count_favorites(self, recipe):
        return recipe.favourites.count()

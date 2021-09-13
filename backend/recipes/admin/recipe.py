from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple
from recipes.models import Recipe, RecipeIngredient


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
        'name',
        'author',
        'last_update',
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

    def get_queryset(self, request):
        return super().get_queryset(request).for_admin_page().with_last_update()

    def get_ordering(self, request):
        return ['-favourites']

    @admin.display(description='последнее обновление')
    def last_update(self, recipe):
        return recipe.last_update

    @admin.display(description='добавлений в избранное')
    def count_favorites(self, recipe):
        return recipe.count_favorites

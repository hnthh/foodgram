from django.contrib import admin
from recipes.models import RecipeIngredient


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient_name',
        'amount_dot',
        'measurement_unit',
    )

    @admin.display(description='ингредиент')
    def ingredient_name(self, recipeingredient):
        return recipeingredient.ingredient.name

    @admin.display(description='количество')
    def amount_dot(self, recipeingredient):
        return str(recipeingredient.amount).replace(',', '.')

    @admin.display(description='единица измерения')
    def measurement_unit(self, recipeingredient):
        return recipeingredient.ingredient.measurement_unit

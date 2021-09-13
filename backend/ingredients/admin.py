from config.admin import AppAdmin, admin
from ingredients.models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(AppAdmin):
    list_display = ('name', 'measurement_unit')

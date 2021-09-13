from django.contrib import admin
from recipes.models import ShoppingCart


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_to_purchases')
    fields = ('user', 'recipe')
    readonly_fields = ('user', 'recipe')

    @admin.display(description='добавлено в корзину')
    def added_to_purchases(self, purchase):
        return purchase.created

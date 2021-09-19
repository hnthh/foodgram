from config.admin import AppAdmin, admin
from recipes.models import ShoppingCart


@admin.register(ShoppingCart)
class ShoppingCartAdmin(AppAdmin):
    list_display = ('__str__', 'added_to_purchases')
    fields = ('user', 'recipe')
    readonly_fields = ('user', 'recipe')

    @admin.display(description='добавлено в корзину')
    def added_to_purchases(self, purchase):
        return purchase.created

    def get_readonly_fields(self, request, purchase=None):
        if purchase is not None:
            return ('user', 'recipe')
        return tuple()

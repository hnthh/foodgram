from django.contrib import admin
from recipes.models import ShoppingCart


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from recipes.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from recipes.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'added_to_favourites')
    fields = ('user', 'recipe')
    readonly_fields = ('user', 'recipe')

    @admin.display(description='добавлено в избранное')
    def added_to_favourites(self, favorite):
        return favorite.created

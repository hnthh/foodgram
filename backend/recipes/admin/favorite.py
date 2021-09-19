from config.admin import AppAdmin, admin
from recipes.models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(AppAdmin):
    list_display = ('__str__', 'added_to_favourites')
    fields = ('user', 'recipe')
    readonly_fields = ('user', 'recipe')

    @admin.display(description='добавлено в избранное')
    def added_to_favourites(self, favorite):
        return favorite.created

    def get_readonly_fields(self, request, favorite=None):
        if favorite is not None:
            return ('user', 'recipe')
        return tuple()

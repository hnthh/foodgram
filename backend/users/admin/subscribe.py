from config.admin import AppAdmin, admin
from users.models import Subscribe


@admin.register(Subscribe)
class SubscribeAdmin(AppAdmin):
    list_display = ('__str__', 'subscribe_date')
    fields = ('user', 'author')
    readonly_fields = ('user', 'author')

    @admin.display(description='дата подписки')
    def subscribe_date(self, subscription):
        return subscription.created

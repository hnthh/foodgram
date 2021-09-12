from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy
from users.models import Subscribe, User

admin.site.unregister(TokenProxy)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    pass

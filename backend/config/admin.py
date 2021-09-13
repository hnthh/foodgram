from django.contrib import admin


class AppAdmin(admin.ModelAdmin):
    empty_value_display = '—'

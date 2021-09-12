from django.contrib import admin
from tags.models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'color_name',
        'color_hex',
    )

    @admin.display(description='HEX')
    def color_hex(self, tag):
        return tag.color

    @admin.display(description='Название цвета')
    def color_name(self, tag):
        return tag.color_name

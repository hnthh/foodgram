from collections import namedtuple

from django.core.management.base import BaseCommand
from tags.models import Tag

TagNamed = namedtuple('TagNamed', 'name color slug')

TAGS = [
    TagNamed('Завтрак', '#4f738e', 'breakfast'),
    TagNamed('Обед', '#c87f89', 'lunch'),
    TagNamed('Ужин', '#a484ac', 'dinner'),
]


class Command(BaseCommand):

    def handle(self, *args, **options):

        for tag in TAGS:
            Tag.objects.get_or_create(
                name=tag.name,
                color=tag.color,
                slug=tag.slug,
            )

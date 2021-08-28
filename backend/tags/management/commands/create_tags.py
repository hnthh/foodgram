from collections import namedtuple

from django.core.management.base import BaseCommand
from tags.models import Tag

TagNamed = namedtuple('TagNamed', 'name color slug')

TAGS = [
    TagNamed('Завтрак', '#FFB500', 'breakfast'),
    TagNamed('Обед', '#F93800', 'lunch'),
    TagNamed('Ужин', '#283350', 'dinner'),
]


class Command(BaseCommand):

    def handle(self, *args, **options):

        for tag in TAGS:
            Tag.objects.get_or_create(
                name=tag.name,
                color=tag.color,
                slug=tag.slug,
            )

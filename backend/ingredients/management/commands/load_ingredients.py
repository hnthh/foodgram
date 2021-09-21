import csv
import re

from django.core.management.base import BaseCommand, CommandError
from ingredients.models import Ingredient


class Command(BaseCommand):
    help = "Creates Ingredient's model instances with data from a csv file"

    def handle(self, *args, **options):
        try:
            file = open('ingredients/data/ingredients.csv')  # noqa: SIM115
        except OSError:
            raise CommandError('Could not open ingredients.csv file')

        with file:
            reader = csv.reader(file)

            ingredients = list()
            for row in reader:
                *parts, unit = row

                name = ','.join(parts)  # handle: 'вишня, протертая с сахаром'
                name = re.sub(
                    r'(?<=\d),(?=\d)', '.', name,
                )  # handle: 'молоко 3.6%'

                ingredient = Ingredient(name=name, measurement_unit=unit)
                ingredients.append(ingredient)

            Ingredient.objects.bulk_create(ingredients, ignore_conflicts=True)

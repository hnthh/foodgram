import csv

from django.core.management.base import BaseCommand, CommandError
from ingredients.models import Ingredient


class Command(BaseCommand):
    help = "Creates Ingredient's model instances with data from a csv file"

    def handle(self, *args, **options):
        try:
            file = open('ingredients/data/ingredients.csv')
        except OSError:
            raise CommandError(
                'Could not open ingredients.csv file',
            )

        with file:
            reader = csv.reader(file)

            ingredients = [
                Ingredient(**dict(zip(('name', 'measurement_unit'), row)))
                for row in reader
            ]
            Ingredient.objects.bulk_create(ingredients, ignore_conflicts=True)

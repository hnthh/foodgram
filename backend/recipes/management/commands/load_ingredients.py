import csv

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Creates Ingredient's model instances with data from a csv file"

    def handle(self, *args, **options):
        try:
            file = open('recipes/data/ingredients.csv')
        except OSError:
            raise CommandError(
                'Could not open ingredients.csv file',
            )

        with file:
            reader = csv.reader(file)

            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1],
                )

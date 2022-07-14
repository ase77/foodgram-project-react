from csv import DictReader

from django.core.management import BaseCommand
from recipes.models import Ingredient

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

class_list = (Ingredient,)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for value in class_list:
            if value.objects.exists():
                print(f'''{value.__name__} data already loaded
                {ALREDY_LOADED_ERROR_MESSAGE}
                ''')
            else:
                print(f'Loading {value.__name__} data')

        for row in DictReader(
                open('../data/ingredients.csv', encoding="utf8")):
            if row['name'] not in Ingredient.objects.all():
                ingredients = Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
                ingredients.save()

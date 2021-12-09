import csv
import os

from django.core.management import BaseCommand

from recipes.models import Ingredient, Tag
from users.models import User


class Command(BaseCommand):
    """Загружает csv в базу данных."""

    TABLES_DICT = {User: 'users.csv',
                   Ingredient: 'ingredients.csv',
                   Tag: 'tag.csv',
                   }

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        for table, file in self.TABLES_DICT.items():
            filename = os.path.join(path, file)
            with open(filename, 'r', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    table(**row).save()
        print('Я — Гайбраш Трипвуд, могущественный пират! '
              'Я видел кофейные чашки больше этой базы!')

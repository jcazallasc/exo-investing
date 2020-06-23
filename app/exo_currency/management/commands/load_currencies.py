import csv
import os

from django.core.management.base import BaseCommand, CommandError

from exo_currency.models import Currency


class Command(BaseCommand):
    help = """Load currencies from CSV file. The CSV File must to be inside commands folder."""

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', help='CSV filename', type=str)

    def get_full_path(self, csv_file):
        return os.path.join(os.path.dirname(__file__), csv_file)

    def handle(self, *args, **options):
        csv_filename = options.get('csv_filename')
        csv_file = self.get_full_path(csv_filename)

        try:
            with open(csv_file, mode='r') as csv_file:
                csv_reader = csv.DictReader(
                    csv_file, delimiter=';',
                    quoting=csv.QUOTE_NONE,
                )

                for row in csv_reader:
                    Currency.objects.update_or_create(
                        code=row['code'],
                        defaults={
                            'name': row['name'],
                            'symbol': row['symbol'],
                        },
                    )
        except FileNotFoundError as error:
            raise CommandError(error)

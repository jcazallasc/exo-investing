import csv
import os

from django.core.management.base import BaseCommand, CommandError

from exo_currency.models import Currency, CurrencyExchangeRate


class Command(BaseCommand):
    help = 'Load exchange rates from CSV file. The CSV File must to be inside commands folder.'

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
                    csv_file,
                    quoting=csv.QUOTE_NONE,
                )

                for row in csv_reader:
                    source_currency, _created = Currency.objects.get_or_create(
                        code=row['source_currency'],
                    )

                    exchanged_currency, _created = Currency.objects.get_or_create(
                        code=row['exchanged_currency'],
                    )

                    CurrencyExchangeRate.objects.update_or_create(
                        source_currency=source_currency,
                        exchanged_currency=exchanged_currency,
                        valuation_date=row['valuation_date'],
                        defaults={
                            'rate_value': row['rate_value'],
                        }
                    )
                print('Import exchange rates done!')
        except FileNotFoundError as error:
            raise CommandError(error)

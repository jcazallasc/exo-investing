import csv
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from exo_currency.models import Currency, CurrencyExchangeRate


class CommandsTestCase(TestCase):

    def _get_num_lines_from_csv(self, filename):
        """Return the number of lines in the CSV file inside commands folder"""

        _file = open('/app/exo_currency/management/commands/' + filename)
        _reader = csv.reader(_file)

        return len(list(_reader))

    def test_load_currencies_from_csv(self):
        """Test waiting for db when db is available"""

        filename = 'currencies.csv'

        call_command('load_currencies', filename)

        num_currencies = Currency.objects.all().count()

        self.assertEqual(num_currencies + 1, self._get_num_lines_from_csv(filename))

    def test_load_currencies_from_csv_twice(self):
        """Test waiting for db when db is available"""

        filename = 'currencies.csv'

        call_command('load_currencies', filename)
        call_command('load_currencies', filename)

        num_currencies = Currency.objects.all().count()

        self.assertEqual(num_currencies + 1, self._get_num_lines_from_csv(filename))

    def test_load_exchange_rates_from_csv(self):
        """Test waiting for db when db is available"""

        filename = 'data.csv'

        call_command('load_exchange_rates', filename)

        num_exchange_rates = CurrencyExchangeRate.objects.all().count()

        self.assertEqual(num_exchange_rates + 1, self._get_num_lines_from_csv(filename))

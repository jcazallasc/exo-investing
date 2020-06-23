import csv
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase

from exo_currency.models import Currency, CurrencyExchangeRate, Provider
from exo_currency.utils import CURRENCY_EXCHANGER_PROVIDERS


class CommandsTestCase(TestCase):

    def _get_num_lines_from_csv(self, filename):
        """Return the number of lines in the CSV file inside commands folder"""

        _file = open('/app/exo_currency/management/commands/' + filename)
        _reader = csv.reader(_file)

        return len(list(_reader))

    def test_load_currencies_from_csv(self):
        """Test load currencies from CSV file"""

        filename = 'currencies.csv'

        call_command('load_currencies', filename)

        num_currencies = Currency.objects.all().count()

        self.assertEqual(num_currencies + 1, self._get_num_lines_from_csv(filename))

    def test_load_currencies_from_csv_twice(self):
        """Test load currencies from CSV file twice to check no errors raise"""

        filename = 'currencies.csv'

        call_command('load_currencies', filename)
        call_command('load_currencies', filename)

        num_currencies = Currency.objects.all().count()

        self.assertEqual(num_currencies + 1, self._get_num_lines_from_csv(filename))

    def test_load_exchange_rates_from_csv(self):
        """Test load exchange rates from CSV file"""

        filename = 'data.csv'

        call_command('load_exchange_rates', filename)

        num_exchange_rates = CurrencyExchangeRate.objects.all().count()

        self.assertEqual(num_exchange_rates + 1, self._get_num_lines_from_csv(filename))

    def test_load_exchange_rates_from_csv_twice(self):
        """Test load exchange rates from CSV file twice to check no errors raise"""

        filename = 'data.csv'

        call_command('load_exchange_rates', filename)
        call_command('load_exchange_rates', filename)

        num_exchange_rates = CurrencyExchangeRate.objects.all().count()

        self.assertEqual(num_exchange_rates + 1, self._get_num_lines_from_csv(filename))

    def test_load_providers(self):
        """Test load providers twice to check no errors raise"""

        call_command('load_providers')

        num_providers = Provider.objects.all().count()

        self.assertEqual(num_providers, len(CURRENCY_EXCHANGER_PROVIDERS))

    def test_load_providers_twice(self):
        """Test load providers twice to check no errors raise"""

        call_command('load_providers')
        call_command('load_providers')

        num_providers = Provider.objects.all().count()

        self.assertEqual(num_providers, len(CURRENCY_EXCHANGER_PROVIDERS))

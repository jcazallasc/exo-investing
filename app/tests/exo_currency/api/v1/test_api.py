import json
from datetime import date
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from exo_currency.models import Currency, CurrencyExchangeRate, Provider

CURRENCY_EXCHANGE_RATES_URL = 'currency-exchange-rates'
CALCULATE_AMOUNT_URL = 'calculate-amount'
CALCULATE_TIME_WEIGHTED_RATE_URL = 'calculate-time-weighted-rate'


class ExoCurrencyV1ApiTests(TestCase):
    """Test for the API V1 of exo_currency"""

    def setUp(self):
        self.client = APIClient()

        providers = Provider.objects.all().count()
        if not providers:
            call_command('load_providers')

        currencies = Currency.objects.all().count()
        if not currencies:
            call_command('load_currencies', 'currencies.csv')

        currency_exchange_rates = CurrencyExchangeRate.objects.all().count()
        if not currency_exchange_rates:
            call_command('load_exchange_rates', 'data.csv')

    def test_currency_exchange_rates(self):
        """Test listing currency exchange rates with a valid request"""

        res = self.client.get(reverse(CURRENCY_EXCHANGE_RATES_URL))

        currency_exchange_rates_count = CurrencyExchangeRate.objects.all().count()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], currency_exchange_rates_count)

    def test_currency_exchange_rates_with_from(self):
        """Test listing currency exchange rates with a valid request with from filter"""

        _from = '2020-01-01'
        url = '{}{}'.format(
            reverse(CURRENCY_EXCHANGE_RATES_URL),
            '?from=' + _from,
        )
        res = self.client.get(url)

        currency_exchange_rates_count = CurrencyExchangeRate.objects.filter(valuation_date__gte=_from).count()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], currency_exchange_rates_count)

    def test_currency_exchange_rates_with_to(self):
        """Test listing currency exchange rates with a valid request with to filter"""

        _to = '2020-06-10'
        url = '{}{}'.format(
            reverse(CURRENCY_EXCHANGE_RATES_URL),
            '?to=' + _to,
        )
        res = self.client.get(url)

        currency_exchange_rates_count = CurrencyExchangeRate.objects.filter(valuation_date__lte=_to).count()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], currency_exchange_rates_count)

    def test_currency_exchange_rates_with_from_and_to(self):
        """Test listing currency exchange rates with a valid request with from and to filter"""

        _from = '2020-06-05'
        _to = '2020-06-10'
        url = '{}{}{}'.format(
            reverse(CURRENCY_EXCHANGE_RATES_URL),
            '?from=' + _from,
            '&to=' + _to,
        )
        res = self.client.get(url)

        currency_exchange_rates_count = CurrencyExchangeRate.objects\
            .filter(valuation_date__gte=_from)\
            .filter(valuation_date__lte=_to)\
            .count()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], currency_exchange_rates_count)

    @patch('requests.get')
    def test_calculate_amount(self, mock_get):
        """Test creating user with valid payload is successful"""

        mock_return_value = MagicMock()
        mock_return_value.status_code = 200
        mock_return_value.text = json.dumps({
            'success': True,
            'imestamp': 1363478399,
            'historical': True,
            'base': 'EUR',
            'date': '2020-06-23',
            'rates': {
                    'USD': 1.307716,
            }
        })
        mock_get.return_value = mock_return_value

        url = reverse(
            CALCULATE_AMOUNT_URL,
            kwargs={
                'origin_currency': 'EUR',
                'amount': '5',
                'target_currency': 'USD',
            },
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res.data.get('amount'))

    @patch('requests.get')
    def test_calculate_time_weighted_rate(self, mock_get):
        """Test creating user with valid payload is successful"""

        mock_return_value = MagicMock()
        mock_return_value.status_code = 200
        mock_return_value.text = json.dumps({
            'success': True,
            'imestamp': 1363478399,
            'historical': True,
            'base': 'EUR',
            'date': '2020-06-23',
            'rates': {
                    'USD': 1.307716,
            }
        })
        mock_get.return_value = mock_return_value

        url = reverse(
            CALCULATE_TIME_WEIGHTED_RATE_URL,
            kwargs={
                'origin_currency': 'EUR',
                'amount': '5',
                'target_currency': 'USD',
                'date_invested': '2020-06-20',
            },
        )
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res.data.get('twr'))

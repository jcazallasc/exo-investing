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

EXCHANGE_RATE_EVOLUTION = 'exchange-rate-evolution'


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

    @patch('requests.get')
    def test_exchange_rate_evolution_view_with_no_params(self, mock_get):
        """Test the exchange rate evolution view works with no params"""

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
                'CHF': 1.307716,
                'GBP': 1.307716,
            }
        })
        mock_get.return_value = mock_return_value

        res = self.client.get(reverse(EXCHANGE_RATE_EVOLUTION))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

import json
from unittest.mock import MagicMock, patch

from django.core.management import call_command
from django.test import TestCase

from exo_currency.models import Provider
from exo_currency.utils import CURRENCY_EXCHANGER_PROVIDERS
from exo_currency.utils.base_currency_exchanger import BaseCurrencyExchanger
from exo_currency.utils.fixer_currency_exchanger import FixerCurrencyExchanger
from exo_currency.utils.mock_currency_exchanger import MockCurrencyExchanger


class CurrencyExchangerTest(TestCase):

    def setUp(self):
        counter = Provider.objects.all().count()
        if not counter:
            call_command('load_providers')

    def test_base_exchanger_use_right_provider(self):
        """Test BaseExchange use the provider with lowest order"""

        provider = BaseCurrencyExchanger().provider

        self.assertEqual(FixerCurrencyExchanger.__name__, provider.__name__)

    @patch('requests.get')
    def test_fixer_exchanger_get_rate_once(self, mock_get):
        """Test FixerExchange call to Fixer API"""
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

        rate_value = BaseCurrencyExchanger().get_exchange_rate_data(
            'EUR',
            'USD',
            '2020-06-23',
        )

        self.assertTrue(mock_get.called)
        self.assertEqual(rate_value, 1.307716)

    @patch('requests.get')
    def test_fixer_exchanger_get_rate_twice(self, mock_get):
        """Test FixerExchange just call once to get the rate value, Second time the value is in the db"""
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

        BaseCurrencyExchanger().get_exchange_rate_data('EUR', 'USD', '2020-06-23',)
        BaseCurrencyExchanger().get_exchange_rate_data('EUR', 'USD', '2020-06-23',)

        self.assertEqual(mock_get.call_count, 1)

    def test_base_exchanger_changing_provider_order(self):
        """Test FixerExchange call to Fixer API"""

        provider = BaseCurrencyExchanger().provider
        self.assertEqual(FixerCurrencyExchanger.__name__, provider.__name__)

        fixer_key, fixer_class = CURRENCY_EXCHANGER_PROVIDERS[0]
        mock_key, mock_class = CURRENCY_EXCHANGER_PROVIDERS[1]

        fixer_provider = Provider.objects.get(name=fixer_key)
        fixer_provider.order = 5
        fixer_provider.save()

        mock_provider = Provider.objects.get(name=mock_key)
        mock_provider.order = 1
        mock_provider.save()

        provider = BaseCurrencyExchanger().provider
        self.assertEqual(MockCurrencyExchanger.__name__, provider.__name__)

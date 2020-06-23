from django.db.utils import IntegrityError
from django.test import TestCase

from exo_currency.models import Currency, CurrencyExchangeRate, Provider
from tests.utils import (sample_currency, sample_currency_exchange_rate,
                         sample_provider)


class CurrencyTest(TestCase):

    def test_create_currency_successful(self):
        """Test creating a new currency successful"""
        code = 'EUR'
        currency = sample_currency(code=code)

        self.assertEqual(currency.code, code)

    def test_create_currency_with_no_code(self):
        """Test creating a new currency with no code"""
        code = None

        with self.assertRaises(IntegrityError):
            currency = sample_currency(code=code)

    def test_create_currency_duplicating_code(self):
        """Test creating a new currency duplicating code"""
        code = 'EUR'
        sample_currency(code=code)

        with self.assertRaises(IntegrityError):
            sample_currency(code=code)


class CurrencyExchangeRateTest(TestCase):

    def test_create_currency_exchange_rate_successful(self):
        """Test creating a currency exchange rate successful"""
        currency1 = sample_currency('T1')
        currency2 = sample_currency('T2')
        date = '2020-01-01'
        rate = 1

        currency_exchange_rate = sample_currency_exchange_rate(currency1, currency2, date, rate)

        self.assertEqual(currency_exchange_rate.source_currency, currency1)
        self.assertEqual(currency_exchange_rate.exchanged_currency, currency2)
        self.assertEqual(currency_exchange_rate.valuation_date, date)
        self.assertEqual(currency_exchange_rate.rate_value, rate)

class ProviderTest(TestCase):

    def test_create_provider_successful(self):
        """Test creating a new provider successful"""
        name = 'Mock'
        order = 1
        provider = sample_provider(name=name, order=order)

        self.assertEqual(provider.name, name)
        self.assertEqual(provider.order, order)

    def test_create_provider_duplicated(self):
        """Test creating a new provider duplicated"""
        name = 'Mock'
        order = 1
        sample_provider(name=name, order=order)

        with self.assertRaises(IntegrityError):
            sample_provider(name=name, order=order)

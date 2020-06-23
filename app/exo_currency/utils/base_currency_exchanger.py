from datetime import date, datetime, timedelta
from functools import reduce

from exo_currency.models import Currency, CurrencyExchangeRate, Provider
from exo_currency.utils import CURRENCY_EXCHANGER_PROVIDERS
from exo_currency.utils.load_class import load_class


class BaseCurrencyExchanger:

    def __init__(self):
        self.provider = self._get_provider()

    def get_exchange_rate_data(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: str,
    ) -> float:
        """Get the rate_value from origin_currency to target_currency in the valuation_date"""

        return self.provider().get_exchange_rate_data(
            source_currency,
            exchanged_currency,
            valuation_date,
        )

    def calculate_amount(
        self,
        origin_currency: str,
        target_currency: str,
        amount: str,
    ) -> float:
        """Convert amount from origin_currency to target_currency"""

        rate = self.get_exchange_rate_data(
            origin_currency,
            target_currency,
            date.today(),
        )

        return float(amount) * float(rate)

    def calculate_time_weighted_rate(
        self,
        origin_currency: str,
        amount: str,
        target_currency: str,
        date_invested: str,
    ):
        """
        Responsible of calculate TWR (Time-Weighted Rate of Return)

        Reference: https://www.investopedia.com/terms/t/time-weightedror.asp
        """

        date_invested = datetime.strptime(date_invested, '%Y-%m-%d')
        today = datetime.now()

        delta = today - date_invested

        initial_value = float(amount)
        twr_values = []
        for i in range(delta.days + 1):
            date = date_invested + timedelta(days=i)
            date = date.strftime('%Y-%m-%d')

            rate_value = self.get_exchange_rate_data(
                origin_currency,
                target_currency,
                date,
            )

            end_value = float(amount) * float(rate_value)

            # I'm not sure about the formula... what or where is Cash Flow?
            hp = 1 + ((end_value - initial_value) / initial_value)

            initial_value = end_value

            twr_values.append(hp)

        return reduce((lambda x, y: x * y), twr_values) - 1

    def _get_provider(self):
        """
        Get the provider with lowest order and import its class
        """

        provider = Provider.objects.order_by('order').first()
        _class = dict(CURRENCY_EXCHANGER_PROVIDERS).get(provider.name)
        return load_class(_class)

    def _has_already_rate_value(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: str,
    ) -> CurrencyExchangeRate:
        """
        Check if the rate_value is already in our db for these parameters.
        In that case, returns the CurrencyExchangeRate
        """

        source_currency, _created = Currency.objects.get_or_create(
            code=source_currency,
        )

        exchanged_currency, e_created = Currency.objects.get_or_create(
            code=exchanged_currency,
        )

        return CurrencyExchangeRate.objects.filter(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=valuation_date,
        ).order_by('-id').first()

    def _save_exchange_rate_data(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: str,
        rate_value: float,
    ) -> None:
        """
        Save the rate_value retrieved from the API in the db to avoid the API call next time
        """

        source_currency, _created = Currency.objects.get_or_create(
            code=source_currency,
        )

        exchanged_currency, _created = Currency.objects.get_or_create(
            code=exchanged_currency,
        )

        CurrencyExchangeRate.objects.create(
            source_currency=source_currency,
            exchanged_currency=exchanged_currency,
            valuation_date=valuation_date,
            rate_value=rate_value,
        )

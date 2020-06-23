from random import uniform

from exo_currency.utils.base_currency_exchanger import BaseCurrencyExchanger


class MockCurrencyExchanger(BaseCurrencyExchanger):

    def get_exchange_rate_data(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: str,
    ) -> float:
        """Get the rate_value from origin_currency to target_currency in the valuation_date"""

        return round(uniform(0, 2), 2)

import json
import os

import requests
from rest_framework import status

from exo_currency.utils.base_currency_exchanger import BaseCurrencyExchanger


class FixerCurrencyExchanger(BaseCurrencyExchanger):

    API_URL = os.getenv('FIXER_API_URL')
    API_KEY = os.getenv('FIXER_API_KEY')

    def get_exchange_rate_data(
        self,
        source_currency: str,
        exchanged_currency: str,
        valuation_date: str,
    ) -> float:
        _has_already_rate_value = self._has_already_rate_value(
            source_currency,
            exchanged_currency,
            valuation_date,
        )

        if _has_already_rate_value:
            return _has_already_rate_value.rate_value

        url = '{}/{}?access_key={}&base={}&symbols={}'.format(
            self.API_URL,
            valuation_date,
            self.API_KEY,
            source_currency,
            exchanged_currency,
        )
        response = requests.get(url)

        if response.status_code != status.HTTP_200_OK:
            raise Exception

        json_data = json.loads(response.text)

        if not json_data['success']:
            raise Exception(json_data['error']['type'])

        rate_value = json_data['rates'][exchanged_currency]

        self._save_exchange_rate_data(
            source_currency,
            exchanged_currency,
            valuation_date,
            rate_value,
        )

        return rate_value

import json
from datetime import datetime, timedelta
from typing import List

from django.shortcuts import render

from exo_currency.models import Currency
from exo_currency.utils.base_currency_exchanger import BaseCurrencyExchanger


class ExchangeRateEvolutionView:

    def get(self, request):
        seven_days_before = datetime.now() - timedelta(weeks=1)

        default_currencies = [currency.code for currency in Currency.objects.exclude(code='EUR')]

        _from = request.GET.get('from', seven_days_before.strftime('%Y-%m-%d'))
        _to = request.GET.get('to', datetime.now().strftime('%Y-%m-%d'))
        _origin_currency = request.GET.get('origin_currency', 'EUR')
        _target_currencies = request.GET.getlist('target_currencies', default_currencies)

        return render(request, 'exchange_rate_evolution.html', {
            'currencies': Currency.objects.all(),
            'origin_currency': _origin_currency,
            'target_currencies': _target_currencies,
            'from': _from,
            'to': _to,
            'chart_columns': json.dumps(_target_currencies),
            'chart_data': json.dumps(self._get_chart_data(_origin_currency, _target_currencies, _from, _to))
        })

    def _get_chart_data(
        self,
        _origin_currency: str,
        _target_currencies: str,
        _from: str,
        _to: str,
    ) -> List[List]:
        _from = datetime.strptime(_from, '%Y-%m-%d')
        _to = datetime.strptime(_to, '%Y-%m-%d')

        delta = _to - _from

        results = []
        for i in range(delta.days + 1):
            date = _from + timedelta(days=i)
            date = date.strftime('%Y-%m-%d')

            result_per_day = [date]

            for _target_currency in _target_currencies:
                rate_value = BaseCurrencyExchanger().get_exchange_rate_data(
                    _origin_currency,
                    _target_currency,
                    date,
                )
                result_per_day.append(float(rate_value))

            results.append(result_per_day)

        return results

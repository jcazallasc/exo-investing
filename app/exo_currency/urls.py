from django.urls import path

from exo_currency.views import ExchangeRateEvolutionView

urlpatterns = [
    path(
        'currency-exchange-rates/',
        ExchangeRateEvolutionView().get,
        name='exchange-rate-evolution',
    ),
]

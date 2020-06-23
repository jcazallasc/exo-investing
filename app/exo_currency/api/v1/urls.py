from django.urls import path

from exo_currency.api.v1.views import (CalculateAmountAPIView,
                                       CalculateTimeWeightedRateAPIView,
                                       CurrencyExchangeRateListAPIView)

urlpatterns = [
    path(
        'currency-exchange-rates/',
        CurrencyExchangeRateListAPIView.as_view(),
        name='currency-exchange-rates',
    ),
    path(
        'calculate-amount/<str:origin_currency>/<str:amount>/<str:target_currency>/',
        CalculateAmountAPIView.as_view(),
        name='calculate-amount',
    ),
    path(
        'calculate-time-weighted-rate/<str:origin_currency>/<str:amount>/<str:target_currency>/<str:date_invested>/',
        CalculateTimeWeightedRateAPIView.as_view(),
        name='calculate-time-weighted-rate',
    ),
]

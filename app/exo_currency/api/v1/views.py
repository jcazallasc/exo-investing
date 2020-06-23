from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from exo_currency.api.v1.pagination import SmallSetPagination
from exo_currency.api.v1.serializers import (
    CalculateAmountSerializer, CalculateTimeWeightedRateSerializer,
    CurrencyExchangeRateSerializer)
from exo_currency.models import CurrencyExchangeRate
from exo_currency.utils.base_currency_exchanger import BaseCurrencyExchanger


class CurrencyExchangeRateListAPIView(generics.ListAPIView):
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeRateSerializer
    pagination_class = SmallSetPagination

    def get_queryset(self):
        queryset = self.queryset

        _from = self.request.query_params.get('from')
        if _from:
            queryset = queryset.filter(valuation_date__gte=_from)

        _to = self.request.query_params.get('to')
        if _to:
            queryset = queryset.filter(valuation_date__lte=_to)

        return queryset


class CalculateAmountAPIView(APIView):

    def get(self, request, origin_currency, amount, target_currency):
        amount_calculated = BaseCurrencyExchanger().calculate_amount(
            origin_currency,
            target_currency,
            amount,
        )

        serializer = CalculateAmountSerializer({
            'amount': amount_calculated,
        })

        return Response(serializer.data)


class CalculateTimeWeightedRateAPIView(APIView):

    def get(
        self,
        request,
        origin_currency,
        amount,
        target_currency,
        date_invested,
    ):
        amount_calculated = BaseCurrencyExchanger()\
            .calculate_time_weighted_rate(origin_currency,
                                          amount,
                                          target_currency,
                                          date_invested)

        serializer = CalculateTimeWeightedRateSerializer({
            'twr': amount_calculated,
        })

        return Response(serializer.data)

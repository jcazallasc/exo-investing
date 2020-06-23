from rest_framework import serializers

from exo_currency.models import Currency, CurrencyExchangeRate


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = '__all__'


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):

    source_currency = CurrencySerializer(read_only=True)
    exchanged_currency = CurrencySerializer(read_only=True)

    class Meta:
        model = CurrencyExchangeRate
        fields = '__all__'


class CalculateAmountSerializer(serializers.Serializer):
    amount = serializers.CharField()


class CalculateTimeWeightedRateSerializer(serializers.Serializer):
    twr = serializers.CharField()

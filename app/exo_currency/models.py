from django.db import models

from exo_currency.utils import CURRENCY_EXCHANGER_PROVIDERS


class Provider(models.Model):
    name = models.CharField(
        max_length=20,
        choices=CURRENCY_EXCHANGER_PROVIDERS,
        unique=True,
    )
    order = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.code


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(
        Currency,
        related_name='exchanges',
        on_delete=models.CASCADE,
    )
    exchanged_currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
    )

    # created is a datetime field, but we could use it as valuation_date
    valuation_date = models.DateField(db_index=True)

    rate_value = models.DecimalField(
        db_index=True,
        decimal_places=6,
        max_digits=18,
    )

    def __str__(self):
        return '{} - {} - {} - {}'.format(
            self.source_currency,
            self.exchanged_currency,
            self.valuation_date,
            self.rate_value,
        )

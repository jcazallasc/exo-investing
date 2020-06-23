from exo_currency.models import Currency, CurrencyExchangeRate, Provider


def sample_currency(code='EUR'):
    return Currency.objects.create(code=code)

def sample_currency_exchange_rate(currency1, currency2, date, rate):
    return CurrencyExchangeRate.objects.create(
        source_currency=currency1,
        exchanged_currency=currency2,
        valuation_date=date,
        rate_value=rate,
    )

def sample_provider(name='Mock', order=1):
    return Provider.objects.create(
        name=name,
        order=order,
    )

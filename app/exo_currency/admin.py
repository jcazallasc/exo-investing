from django.contrib import admin

from exo_currency.models import Currency, CurrencyExchangeRate, Provider

admin.site.register(Currency)
admin.site.register(CurrencyExchangeRate)
admin.site.register(Provider)

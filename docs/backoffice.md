# Exo currency: BackOffice

`http://localhost:8000/backoffice/currency-exchange-rates/`

By default the backoffice loads `EUR` as `origin_currency` and `USD`, `CHF` and `GBP` as target currencies. Also, the data is filtered by last 7 days.

As user, you can change the filter in the left sidebar.

RESTRICTIONS:
- FixerProvider just allow me to do API calls with `EUR` as `origin_currency`.
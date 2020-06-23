# Exo currency
Supports:
- Listing currency exchange rates
- Calculate amount from one currency to another
- Calculate TWR

## Listing currency exchange rates

**Request**:

`GET` `http://localhost:8000/api/v1/currency-exchange-rates/?from=:from&to=:to`

Parameters:

Name      | Type   | Required | Description
----------|--------|----------|------------
from      | string | No       | Date from to use as filter
to        | string | No       | Date to to use as filter

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
200 OK

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 69,
            "source_currency": {
                "id": 1,
                "code": "EUR",
                "name": "Euro",
                "symbol": "€"
            },
            "exchanged_currency": {
                "id": 4,
                "code": "GBP",
                "name": "Pound sterling",
                "symbol": "£"
            },
            "valuation_date": "2020-06-23",
            "rate_value": "0.904762"
        }
    ]
}
```

## Calculate amount from one currency to another

**Request**:

`GET` `http://localhost:8000/api/v1/calculate-amount/:origin_currency/:amount/:target_currency/`

Parameters:

Name                 | Type   | Required | Description
---------------------|--------|----------|------------
origin_currency      | string | Yes      | Currency to convert from
amount               | string | Yes      | Amount to be converted
target_currency      | string | Yes      | Currency to convert to

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
200 OK

{
  "amount": "5.86",
}
```

## Calculate TWR

**Request**:

`GET` `http://localhost:8000/api/v1/calculate-time-weighted-rate/:origin_currency/:amount/:target_currency/:date_invested/`

Parameters:

Name                 | Type   | Required | Description
---------------------|--------|----------|------------
origin_currency      | string | Yes      | Currency to convert from
amount               | string | Yes      | Amount to be converted
target_currency      | string | Yes      | Currency to convert to
date_invested        | string | Yes      | Date the amount was invested

*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
200 OK

{
  "twr": "512.12",
}
```
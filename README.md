## Web service for receiving flights info

### Endpoints:

`GET /flights`

| name          | type      | required | comment
| :------------ | :-------- | :------- | :--------
| `route`       | str       | yes      | Format: _SRC-DST_
| `round_trip`  | bool      | no       | Default: false

**Returns** all flights detailed info or empty list if flight not found

`/flights?route=DXB-BKK&round_trip=true`

```json
[
    {
        "onward": [
            {
                "arrival": "Mon, 22 Oct 2018 04:45:00 GMT",
                "carrier": "AirIndia",
                "departure": "Mon, 22 Oct 2018 00:05:00 GMT",
                "destination": "DEL",
                "flight_number": 996,
                "source": "DXB"
            },
            {
                "arrival": "Mon, 22 Oct 2018 19:35:00 GMT",
                "carrier": "AirIndia",
                "departure": "Mon, 22 Oct 2018 13:50:00 GMT",
                "destination": "BKK",
                "flight_number": 332,
                "source": "DEL"
            }
        ],
        "return": [
            {
                "arrival": "Tue, 30 Oct 2018 12:05:00 GMT",
                "carrier": "AirIndia",
                "departure": "Tue, 30 Oct 2018 08:50:00 GMT",
                "destination": "DEL",
                "flight_number": 333,
                "source": "BKK"
            },
            {
                "arrival": "Tue, 30 Oct 2018 22:45:00 GMT",
                "carrier": "AirIndia",
                "departure": "Tue, 30 Oct 2018 20:40:00 GMT",
                "destination": "DXB",
                "flight_number": 995,
                "source": "DEL"
            }
        ],
        "total_price": 546.8
    }
]
```

---

`GET /top`

| name          | type      | required | comment
| :------------ | :-------- | :------- | :--------
| `route`       | str       | yes      | Format: _SRC-DST_
| `key`         | str       | yes      | Possible values: min_price, max_price, min_length, max_length, optimal
| `round_trip`  | bool      | no       | Default: false

**Returns** one flight detailed info or empty list if flight not found

`/top?route=DXB-BKK&key=optimal`

```json
{
    "onward": [
        {
            "arrival": "Sat, 27 Oct 2018 04:45:00 GMT",
            "carrier": "AirIndia",
            "departure": "Sat, 27 Oct 2018 00:05:00 GMT",
            "destination": "DEL",
            "flight_number": 996,
            "source": "DXB"
        },
        {
            "arrival": "Sat, 27 Oct 2018 19:20:00 GMT",
            "carrier": "AirIndia",
            "departure": "Sat, 27 Oct 2018 13:25:00 GMT",
            "destination": "BKK",
            "flight_number": 332,
            "source": "DEL"
        }
    ],
    "return": [],
    "total_price": 382.7
}
```

---

`GET /compare`

| name          | type      | required | comment
| :------------ | :-------- | :------- | :--------
| `route`       | str       | yes      | Format: _SRC-DST_
| `route2`      | str       | yes      | Format: _SRC-DST_
| `round_trip`  | bool      | no       | Default: false

**Returns** difference between key values of two flights or empty list if flight not found

`/compare?route=DXB-BKK&route2=DWC-BKK`

```json
[
    {
        "max_length_diff": 165,
        "max_price_diff": 4078.2,
        "min_length_diff": 125,
        "min_price_diff": 83.6,
        "number_of_flights_diff": 138
    }
]
```

### Internal structure:

`parser.py` creates two hash tables: `full_info` and `summary_info` that have following structure:

```python
summary_info= {
    'SVO-JFK': {
        'ids': [1, 3, 4],
        'min_price': {'id': 3, 'val': 120},
        'max_price': {'id': 1, 'val': 199},
        'min_length': {'id': 1, 'val': 1075},
        'max_length': {'id': 3, 'val': 1265},
        'optimal_id': 4
    },
    ...
}

full_info = {
    1: {'onward': [{'source': '', 'destination': ''}, {'source': '', 'destination': ''}, ...],
        'return': [{'source': '', 'destination': ''}, {'source': '', 'destination': ''}, ...],
        'total_price': 199},
    ...
}
```

In order to find an optimal flight, following algorithm is used:

1. Get sorted (min to max) dict of pairs id-price;
2. Get sorted (min to max) dict of pairs id-length;
3. Iterate through first dict, find index of current flight in second dict;
4. Save sum of indexes for each id into result dict;
5. Optimal flight is the one that has minimal sum of indexes;

```python
"""
    price | time
1:  800   | 320 
2:  500   | 180
3:  600   | 330
4:  950   | 510
"""

prices = {2: 500, 3: 600, 1: 800, 4: 950}
times = {2: 180, 1: 320, 3: 330, 4: 510}
result = {2: 0, 3: 3, 1: 3, 4: 6}  # {id: sum_of_indexes}
# Optimal flight id: 2

```

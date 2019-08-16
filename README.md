## Web service for receiving flights info.

### Endpoints:

`GET /flights`

`GET /top`

`GET /compare`

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

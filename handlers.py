from functools import lru_cache
from parser import parse_data


@lru_cache()
def get_data(round_trip: bool) -> tuple:
    return parse_data(round_trip)


def flights(route, round_trip=False):
    full_info, summary_info = get_data(round_trip)
    route = route.upper()

    ids = summary_info.get(route, {}).get('ids', {})
    all_flights = [full_info.get(f, '') for f in ids if f in ids]
    return all_flights


def top(route, key, round_trip=False):
    full_info, summary_info = get_data(round_trip)
    route = route.upper()

    if key == 'optimal':
        flight_id = summary_info.get(route, {}).get('optimal_id', {})
    else:
        flight_id = summary_info.get(route, {}).get(key, {}).get('id')
    return full_info.get(flight_id, {})


def compare(route, route2, round_trip=False):
    full_info, summary_info = get_data(round_trip)
    route = route.upper()
    route2 = route2.upper() if route2 else None

    lhs, rhs = summary_info.get(route), summary_info.get(route2)
    if not all((lhs, rhs)):
        return list()
    params, result = ('min_price', 'max_price', 'min_length', 'max_length'), dict()
    for param in params:
        result[f'{param}_diff'] = round(abs(lhs[param]['val'] - rhs[param]['val']), 2)
    result['number_of_flights_diff'] = abs(len(lhs['ids']) - len(rhs['ids']))
    return [result]

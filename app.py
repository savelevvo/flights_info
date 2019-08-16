from flask import Flask, request, jsonify, abort
from functools import lru_cache
from parser import parse_data

app = Flask('flights_info')


@lru_cache()
def get_data(round_trip: bool) -> tuple:
    return parse_data(round_trip)


def handler(route, route2=None, key=None, round_trip=False) -> list:
    full_info, summary_info = get_data(round_trip)
    route = route.upper()
    route2 = route2.upper() if route2 else None

    if key:
        if key == 'optimal':
            flight_id = summary_info.get(route, {}).get('optimal_id', {})
        else:
            flight_id = summary_info.get(route, {}).get(key, {}).get('id')
        return full_info.get(flight_id, {})

    if route2:
        lhs, rhs = summary_info.get(route), summary_info.get(route2)
        if not all((lhs, rhs)):
            return list()
        params, result = ('min_price', 'max_price', 'min_length', 'max_length'), dict()
        for param in params:
            result[f'{param}_diff'] = round(abs(lhs[param]['val'] - rhs[param]['val']), 2)
        result['number_of_flights_diff'] = abs(len(lhs['ids']) - len(rhs['ids']))
        return [result]

    else:
        ids = summary_info.get(route, {}).get('ids', {})
        all_flights = [full_info.get(f, '') for f in ids if f in ids]
        return all_flights


@app.route('/flights', methods=['GET'])
def flights():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :param bool round_trip: Search among one-way flights or round flights. Default: one-way
    :return: all flights from -> to
    """

    if request.method == 'GET':
        _route = request.args.get('route')
        _round = request.args.get('round_trip', False)
        if not _route:
            abort(400)
        result = handler(_route, round_trip=_round)
        return jsonify(result)


@app.route('/top', methods=['GET'])
def top():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :param str key: Sorting key. Possible values: min_price, max_price, min_length, max_length, optimal
    :param bool round_trip: Search among one-way flights or round flights. Default: one-way
    :return: flight info
    """

    if request.method == 'GET':
        _route, _key = request.args.get('route'), request.args.get('key')
        _round = request.args.get('round_trip', False)
        if not all((_route, _key)):
            abort(400)
        result = handler(_route, key=_key, round_trip=_round)
        return jsonify(result)


@app.route('/compare', methods=['GET'])
def compare():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :param str route2: Source and destination airports code. Format: SRC-DST
    :param bool round_trip: Search among one-way flights or round flights. Default: one-way
    :return: list of summary diffs
    """

    if request.method == 'GET':
        _route, _route2 = request.args.get('route'), request.args.get('route2')
        _round = request.args.get('round_trip', False)
        if not all((_route, _route2)):
            abort(400)
        result = handler(_route, route2=_route2, round_trip=_round)
        return jsonify(result)


if __name__ == '__main__':
    app.run()

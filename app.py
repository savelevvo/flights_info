from flask import Flask, request, jsonify, abort
from functools import lru_cache
from parser import parse_data

app = Flask('flights_info')


@lru_cache()
def get_data():
    return parse_data()


def handler(route, route2=None, key=None) -> list:
    full_info, summary_info = get_data()
    all_flights_ids = summary_info[route]['ids']

    if key:
        if key == 'optimal':
            flight_id = summary_info[route]['optimal_id']
        else:
            flight_id = summary_info[route][key]['id']
        return full_info[flight_id]

    if route2:
        lhs, rhs = summary_info[route], summary_info[route2]
        return [{
            'more_flights': abs(len(lhs['ids']) - len(rhs['ids'])),
            'min_price_diff': round(abs(lhs['min_price']['val'] - rhs['min_price']['val']), 2),
            'max_price_diff': round(abs(lhs['max_price']['val'] - rhs['max_price']['val']), 2),
            'min_length_diff': round(abs(lhs['min_length']['val'] - rhs['min_length']['val']), 2),
            'max_length_diff': round(abs(lhs['max_length']['val'] - rhs['max_length']['val']), 2)
        }]

    else:
        all_flights_info = [full_info[f] for f in all_flights_ids if f in all_flights_ids]
        return all_flights_info


@app.route('/flights', methods=['GET'])
def flights():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :return: all flights from -> to
    """

    if request.method == 'GET':
        _route = request.args.get('route')
        if not _route:
            abort(400)
        result = handler(_route)
        return jsonify(result)


@app.route('/top', methods=['GET'])
def top():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :param str key: Sorting key. Possible values: min_price, max_price, min_length, max_length, optimal
    :return: flight info
    """

    if request.method == 'GET':
        _route, _key = request.args.get('route'), request.args.get('key')
        if not all((_route, _key)):
            abort(400)
        result = handler(_route, key=_key)
        return jsonify(result)


@app.route('/compare', methods=['GET'])
def compare():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :param str route2: Source and destination airports code. Format: SRC-DST
    :return: list of summary diffs
    """

    if request.method == 'GET':
        _route, _route2 = request.args.get('route'), request.args.get('route2')
        if not all((_route, _route2)):
            abort(400)
        result = handler(_route, _route2)
        return jsonify(result)


if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify, abort
from parser import parse_data
from functools import lru_cache

app = Flask('flights_info')


@lru_cache()
def get_data():
    return parse_data()


def get_flights(route, route2=None, key=None) -> list:
    full_flights_info, for_search = get_data()
    all_flights_ids = for_search[route]['ids']

    if key:
        if key == 'optimal':
            flight_id = for_search[route]['optimal_id']
        else:
            flight_id = for_search[route][key]['id']
        return full_flights_info[flight_id]

    if route2:
        lhs, rhs = for_search[route], for_search[route2]
        return [{
            'more_flights': abs(len(lhs['ids'])-len(rhs['ids'])),
            'min_price_diff': round(abs(lhs['min_price']['val']-rhs['min_price']['val']), 2),
            'max_price_diff': round(abs(lhs['max_price']['val']-rhs['max_price']['val']), 2),
            'min_length_diff': round(abs(lhs['min_length']['val']-rhs['min_length']['val']), 2),
            'max_length_diff': round(abs(lhs['max_length']['val']-rhs['max_length']['val']), 2)
        }]

    else:
        all_flights_info = [full_flights_info[f] for f in all_flights_ids if f in all_flights_ids]
        return all_flights_info


@app.route('/get-airports', methods=['GET'])
def get_airports():
    """
    :param str route: Source and destination airports code: SRC-DST
    :return: list of all flights from -> to
    """
    if request.method == 'GET':
        route = request.args.get('route')
        if not route:
            abort(400)
        result = get_flights(route)
        return jsonify(result)


@app.route('/get-top', methods=['GET'])
def get_top():
    """
    :param str route: Source and destination airports code: SRC-DST
    :param str key: Sorting key. Possible values: min_price, max_price,
                                                min_length, max_length,
                                                optimal
    :return: top flight info
    """
    if request.method == 'GET':
        route, _key = request.args.get('route'), request.args.get('key')
        if not all((route, _key)):
            abort(400)
        result = get_flights(route, key=_key)
        return jsonify(result)


@app.route('/compare', methods=['GET'])
def compare():
    """

    :return:
    """
    if request.method == 'GET':
        route, route2 = request.args.get('route'), request.args.get('route2')
        if not all((route, route2)):
            abort(400)
        result = get_flights(route, route2)
        return jsonify(result)


if __name__ == '__main__':
    app.run()

from flask import Flask, request, jsonify, abort
from parser import parse_data
from functools import lru_cache

app = Flask('flights_info')


@lru_cache()
def get_flights(_from, _to, _key=None) -> list:
    full_flights_info, for_search = parse_data()
    all_flights_ids = for_search[f'{_from}-{_to}']['ids']

    if _key:
        if _key == 'optimal':
            flight_id = for_search[f'{_from}-{_to}']['optimal_id']
        else:
            flight_id = for_search[f'{_from}-{_to}'][_key]['id']
        return full_flights_info[flight_id]
    else:
        all_flights_info = [full_flights_info[f] for f in all_flights_ids if f in all_flights_ids]
        return all_flights_info


@app.route('/get-airports', methods=['GET'])
def get_airports():
    """
    :param str from: Source airport code
    :param str to: Destination airport code
    :return: list of all flights from -> to
    """
    if request.method == 'GET':
        _from, _to = request.args.get('from'), request.args.get('to')
        if not (_from and _to):
            abort(400)
        result = get_flights(_from, _to, request.args.get('key'))
        return jsonify(result)


# @app.route('/get-top', methods=['GET'])
# def get_top():
#     """
#     :param str from: Source airport code
#     :param str to: Destination airport code
#     :param str key: Sorting key. Possible values: min_price, max_price,
#                                                 min_length, max_length,
#                                                 optimal
#     :return: top flight info
#     """
#     if request.method == 'GET':
#         _from, _to, _key = request.args.get('from'), request.args.get('to'), request.args.get('key')
#         if not all((_from, _to, _key)):
#             abort(400)


# @app.route('/compare', methods=['GET'])
# def compare():
#     """
#
#     :return:
#     """
#     if request.method == 'GET':
#         pass


if __name__ == '__main__':
    app.run()

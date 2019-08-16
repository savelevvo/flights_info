from flask import request, jsonify, abort, Blueprint
import handlers

flight_info = Blueprint('flight_info', __name__)


@flight_info.route('/flights', methods=['GET'])
def flights():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :param bool round_trip: Search among one-way flights or round flights. Default: one-way
    :return: all flights from -> to
    """

    if request.method == 'GET':
        route = request.args.get('route')
        round_trip = request.args.get('round_trip', False)
        if not route:
            abort(400)
        result = handlers.flights(route, round_trip=round_trip)
        return jsonify(result)


@flight_info.route('/top', methods=['GET'])
def top():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :param str key: Sorting key. Possible values: min_price, max_price, min_length, max_length, optimal
    :param bool round_trip: Search among one-way flights or round flights. Default: one-way
    :return: flight info
    """

    if request.method == 'GET':
        route, key = request.args.get('route'), request.args.get('key')
        round_trip = request.args.get('round_trip', False)
        if not all((route, key)):
            abort(400)
        result = handlers.top(route, key, round_trip=round_trip)
        return jsonify(result)


@flight_info.route('/compare', methods=['GET'])
def compare():
    """
    :param str route: Source and destination airports code. Format: SRC-DST
    :param str route2: Source and destination airports code. Format: SRC-DST
    :param bool round_trip: Search among one-way flights or round flights. Default: one-way
    :return: list of summary diffs
    """

    if request.method == 'GET':
        route, route2 = request.args.get('route'), request.args.get('route2')
        round_trip = request.args.get('round_trip', False)
        if not all((route, route2)):
            abort(400)
        result = handlers.compare(route, route2, round_trip=round_trip)
        return jsonify(result)

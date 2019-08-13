from flask import Flask, request, jsonify, abort
from parser import parse_data

app = Flask('flights_info')


def get_flights(_from, _to: str) -> dict:
    return parse_data()


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
        result = get_flights(_from, _to)
        return jsonify(result)


@app.route('/get-top', methods=['GET'])
def get_top():
    """
    :param str from: Source airport code
    :param str to: Destination airport code
    :param str key: Sorting key. Possible values: min_price, max_price,
                                                min_length, max_length,
                                                optimal
    :return: top flight info
    """
    if request.method == 'GET':
        _from, _to, _key = request.args.get('from'), request.args.get('to'), request.args.get('key')
        if not all((_from, _to, _key)):
            abort(400)


@app.route('/compare', methods=['GET'])
def compare():
    """

    :return:
    """
    if request.method == 'GET':
        pass


if __name__ == '__main__':
    app.run()

import xml.etree.ElementTree as ET
from datetime import datetime
from collections import defaultdict


def parse_data(round_trip=False) -> tuple:
    """
    Parses xml file and stores flights info in two hash tables:
    full_info: hash table containing full description of a flight
    summary_info: hash table for searching min/max values
    :return: tuple of above tables
    """

    filename = 'RS_Via-3.xml' if round_trip else 'RS_ViaOW.xml'
    tree = ET.parse(f'xml/{filename}')
    root = tree.getroot()
    flights = root.find('PricedItineraries')

    full_info, summary_info = dict(), dict()
    _prices, _times, _optimals = dict(), dict(), dict()

    for _id, flight in enumerate(flights):
        onward_segments, return_segments = list(), list()
        total_length, prev_arrival = defaultdict(int), defaultdict(int)

        onward_flights = flight.findall("./OnwardPricedItinerary//Flight")
        return_flights = flight.findall("./ReturnPricedItinerary//Flight")
        total_price = float(flight.find("./Pricing//*[@ChargeType='TotalAmount']").text)
        first_airport = onward_flights[0].find('Source').text
        last_airport = onward_flights[-1].find('Destination').text

        for direction, value in {'onward': onward_flights, 'return': return_flights}.items():
            for flight_segment in value:
                carrier = flight_segment.find('Carrier').text
                flight_n = int(flight_segment.find('FlightNumber').text)
                source = flight_segment.find('Source').text
                destination = flight_segment.find('Destination').text
                departure = datetime.strptime(flight_segment.find('DepartureTimeStamp').text, "%Y-%m-%dT%H%M")
                arrival = datetime.strptime(flight_segment.find('ArrivalTimeStamp').text, "%Y-%m-%dT%H%M")

                total_length[direction] += int((arrival - departure).total_seconds() / 60)
                if prev_arrival[direction]:
                    total_length[direction] += int((departure - prev_arrival[direction]).total_seconds() / 60)

                prev_arrival[direction] = arrival

                segment = {'carrier': carrier, 'flight_number': flight_n, 'source': source, 'destination': destination,
                           'departure': departure, 'arrival': arrival}

                if direction == 'onward':
                    onward_segments.append(segment)
                elif direction == 'return':
                    return_segments.append(segment)

        total_length = sum(total_length.values())

        route = f'{first_airport}-{last_airport}'
        _prices.setdefault(route, {})[_id] = total_price
        _times.setdefault(route, {})[_id] = total_length

        summary_info.setdefault(route, {}).setdefault('ids', []).append(_id)
        full_info[_id] = {'onward': onward_segments, 'return': return_segments, 'total_price': total_price}

    # assert records in xml are sorted by price from min to max
    # sort time from min to max
    for route in _times:
        _times[route] = dict(sorted(_times[route].items(), key=lambda v: v[1]))

    # find optimal id
    for route in _prices:
        for _id, _ in _prices[route].items():
            index_price = list(_prices[route].keys()).index(_id)
            index_time = list(_times[route].keys()).index(_id)
            _optimals.setdefault(route, []).append({_id: index_price + index_time})

    for route in summary_info:
        price_values = list(_prices[route].items())
        time_values = list(_times[route].items())
        value_map = {
            'min_price': price_values[0],
            'max_price': price_values[-1],
            'min_length': time_values[0],
            'max_length': time_values[-1]
        }
        for k, v in value_map.items():
            summary_info[route].setdefault(k, dict(zip(('id', 'val'), v)))
        optimal_id = next(iter(_optimals[route][0]))
        summary_info[route].setdefault('optimal_id', optimal_id)

    return full_info, summary_info

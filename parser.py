import xml.etree.ElementTree as ET
from datetime import datetime


def parse_data() -> tuple:
    """
    Parses xml file and stores flights info in two hash tables:
    full_flights_info: contains full description of a flight
    for_search: optimized for searching min/max values
    :return: tuple of above tables
    """

    tree = ET.parse('xml/RS_Via-3.xml')
    root = tree.getroot()
    flights = root.find('PricedItineraries')
    full_flights_info, for_search = dict(), dict()

    for _id, flight in enumerate(flights):
        onward_flights = flight.findall("./OnwardPricedItinerary//Flight")
        return_flights = flight.findall("./ReturnPricedItinerary//Flight")
        # flight_segments = flight.findall(".//Flight")

        total_price = float(flight.find("./Pricing//*[@ChargeType='TotalAmount']").text)

        onward_segments = list()

        first_airport = onward_flights[0].find('Source').text
        last_airport = onward_flights[-1].find('Destination').text

        first_length = datetime.strptime(onward_flights[0].find('DepartureTimeStamp').text, "%Y-%m-%dT%H%M")
        last_length = datetime.strptime(onward_flights[-1].find('ArrivalTimeStamp').text, "%Y-%m-%dT%H%M")
        total_length = int(((last_length - first_length).total_seconds()) / 60)  # minutes

        for flight_segment in onward_flights:
            carrier = flight_segment.find('Carrier').text
            flight_n = int(flight_segment.find('FlightNumber').text)
            source = flight_segment.find('Source').text
            destination = flight_segment.find('Destination').text
            departure = datetime.strptime(flight_segment.find('DepartureTimeStamp').text, "%Y-%m-%dT%H%M")
            arrival = datetime.strptime(flight_segment.find('ArrivalTimeStamp').text, "%Y-%m-%dT%H%M")

            segment = {'carrier': carrier, 'flight_number': flight_n, 'source': source, 'destination': destination,
                       'departure': departure, 'arrival': arrival}
            onward_segments.append(segment)

        route = f'{first_airport}-{last_airport}'

        # get all flight ids for current flight
        for_search.setdefault(route, {}).setdefault('ids', []).append(_id)

        # get min/max price values
        if total_price < for_search[route].setdefault('min_price', {'id': _id, 'val': total_price})['val']:
            for_search[route]['min_price'] = {'id': _id, 'val': total_price}
        if total_price > for_search[route].setdefault('max_price', {'id': _id, 'val': total_price})['val']:
            for_search[route]['max_price'] = {'id': _id, 'val': total_price}

        # get min/max time
        if total_length < for_search[route].setdefault('min_length', {'id': _id, 'val': total_length})['val']:
            for_search[route]['min_length'] = {'id': _id, 'val': total_length}
        if total_length > for_search[route].setdefault('max_length', {'id': _id, 'val': total_length})['val']:
            for_search[route]['max_length'] = {'id': _id, 'val': total_length}

        full_flights_info[_id] = {'onward': onward_segments, 'total_price': total_price}

    print(for_search)
    return full_flights_info, for_search

parse_data()


"""

for_search = {
    'SVO-JFK': {
        'ids': [1, 3, 4],
        'min_price': {'id': 3, 'val': 120},
        'max_price': {'id': 1, 'val': 199},
        'shortest': {'id': 1, 'val': '10h'},
        'longest': {'id': 3, 'val': '14h'},
        'optimal_id': 2
    },
    '': {}
}

full_flights_info = {
    1: {...},
    2: {'onward': [{'from': '', 'to': ''}, {'from': '', 'to': ''}],
        'return': [{'from': '', 'to': ''}, {'from': '', 'to': ''}],
        'total_price': 199}
}

"""

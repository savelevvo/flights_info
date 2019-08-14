import xml.etree.ElementTree as ET
from datetime import datetime, timedelta


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
        flight_summary = dict()

        current_min_price = total_price
        current_max_price = 0
        current_min_time = timedelta(days=99)
        current_max_time = timedelta(seconds=0)
        segment_time = timedelta(seconds=0)
        end_time = datetime(year=9999, month=1, day=1)
        total_time = timedelta(seconds=0)

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

            ##############################

            segment_time += arrival - departure
            if end_time.year == 9999:
                end_time = arrival
            else:
                total_time = segment_time + (departure - end_time)

            route = f'{source}-{destination}'
            min_price = min(total_price, current_min_price)
            current_min_price = min_price

            max_price = max(total_price, current_max_price)
            current_max_price = max_price

            shortest = min(total_time, current_min_time)
            current_min_time = shortest

            longest = max(total_time, current_max_time)
            current_max_time = longest

            optimal = None

            flight_summary = {
                route: {
                    'ids': _id,
                    'min_price': {'id': _id, 'val': min_price},
                    'max_price': {'id': _id, 'val': max_price},
                    'shortest': {'id': _id, 'val': shortest},
                    'longest': {'id': _id, 'val': longest},
                    'optimal': optimal
                }
            }

        full_flights_info[_id] = {'onward': onward_segments, 'total_price': total_price}

        for_search.update(flight_summary)
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

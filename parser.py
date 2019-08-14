import xml.etree.ElementTree as ET
from collections import defaultdict


def parse_data() -> tuple:
    """
    Parses xml file and stores flights info in two hash tables:
    full_flights_info: contains full description of a flight
    for_search: optimized for searching min/max values
    :return: tuple of above tables
    """

    tree = ET.parse('xml/RS_Via-3.xml')
    root = tree.getroot()
    full_flights_info = dict()
    for_search = dict()
    values = defaultdict(int)

    flights = root.find('PricedItineraries')
    for _id, flight in enumerate(flights):
        # _onward = flight.findall("./OnwardPricedItinerary//Flight")
        # _return = flight.findall("./ReturnPricedItinerary//Flight")
        flight_segments = flight.findall(".//Flight")
        total_price = float(flight.find("./Pricing//*[@ChargeType='TotalAmount']").text)

        full_flights_info[_id]['total_price'] = total_price
        for flight_segment in flight_segments:
            source = ''
            dest = ''
            full_flights_info[_id] = {
                'source': '',
                'dest': '',
                'intermid': '',
                'carrier': '',
                'flight_n': 0,
                'dep_time': None,
                'arr_time': None
            }

            route_name = f'{source}-{dest}'
            for_search[route_name]['ids'] += _id
            for_search[route_name] = {
                'min_price': {'id': values['min_price']['id'], 'val': values['min_price']['val']},
                'max_price': {'id': values['max_price']['id'], 'val': values['max_price']['val']},
                'short': {'id': values['short']['id'], 'val': values['short']['val']},
                'long': {'id': values['long']['id'], 'val': values['long']['val']},
                'optimal_id': values['optimal_id']
            }

    return full_flights_info, for_search

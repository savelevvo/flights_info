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
    _prices, _times = dict(), dict()
    optimals = dict()

    for _id, flight in enumerate(flights):
        onward_flights = flight.findall("./OnwardPricedItinerary//Flight")
        return_flights = flight.findall("./ReturnPricedItinerary//Flight")
        # flight_segments = flight.findall(".//Flight")

        total_price = float(flight.find("./Pricing//*[@ChargeType='TotalAmount']").text)

        onward_segments, return_segments = list(), list()

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

        if return_flights:
            first_length = datetime.strptime(return_flights[0].find('DepartureTimeStamp').text, "%Y-%m-%dT%H%M")
            last_length = datetime.strptime(return_flights[-1].find('ArrivalTimeStamp').text, "%Y-%m-%dT%H%M")
            total_length += int(((last_length - first_length).total_seconds()) / 60)  # minutes

            for flight_segment in return_flights:
                carrier = flight_segment.find('Carrier').text
                flight_n = int(flight_segment.find('FlightNumber').text)
                source = flight_segment.find('Source').text
                destination = flight_segment.find('Destination').text
                departure = datetime.strptime(flight_segment.find('DepartureTimeStamp').text, "%Y-%m-%dT%H%M")
                arrival = datetime.strptime(flight_segment.find('ArrivalTimeStamp').text, "%Y-%m-%dT%H%M")

                segment = {'carrier': carrier, 'flight_number': flight_n, 'source': source, 'destination': destination,
                           'departure': departure, 'arrival': arrival}
                return_segments.append(segment)

        route = f'{first_airport}-{last_airport}'
        _prices.setdefault(route, {})[_id] = total_price
        _times.setdefault(route, {})[_id] = total_length

        # get all flight ids for current flight
        for_search.setdefault(route, {}).setdefault('ids', []).append(_id)

        full_flights_info[_id] = {'onward': onward_segments, 'return': return_segments, 'total_price': total_price}

    # assert _prices is sorted by price from min to max
    # sort time from min to max
    for k in _times:
        _times[k] = dict(sorted(_times[k].items(), key=lambda v: v[1]))

    for route_name in _prices:
        for _id, _ in _prices[route_name].items():
            index_price = list(_prices[route_name].keys()).index(_id)
            index_time = list(_times[route_name].keys()).index(_id)
            optimals.setdefault(route_name, []).append({_id: index_price + index_time})

    for k in for_search:
        min_price, max_price = list(_prices[k].items())[0], list(_prices[k].items())[-1]
        min_length, max_length = list(_times[k].items())[0], list(_times[k].items())[-1]
        optimal_id = next(iter(optimals[k][0]))
        for_search[k].setdefault('min_price', dict(zip(('id', 'val'), min_price)))
        for_search[k].setdefault('max_price', dict(zip(('id', 'val'), max_price)))
        for_search[k].setdefault('min_length', dict(zip(('id', 'val'), min_length)))
        for_search[k].setdefault('max_length', dict(zip(('id', 'val'), max_length)))
        for_search[k].setdefault('optimal_id', optimal_id)

    return full_flights_info, for_search

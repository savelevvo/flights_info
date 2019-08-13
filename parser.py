import xml.etree.ElementTree as ET


def parse_data():
    tree = ET.parse('xml/RS_Via-3.xml')
    root = tree.getroot()

    flights = root.find('PricedItineraries')
    for _id, flight in enumerate(flights):
        _onward = flight.findall("./OnwardPricedItinerary//Flight")
        _return = flight.findall("./ReturnPricedItinerary//Flight")
        # _all_flights = flight.findall(".//Flight")
        total_price = float(flight.find("./Pricing//*[@ChargeType='TotalAmount']").text)

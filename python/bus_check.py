import logging
import requests
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

class BusClient ():
    """Class for api requests to Tautulli"""
    BASE_URL = ""

    def get(self):
        """Get request"""
        url = f'{self.BASE_URL}'
        return requests.get(url, verify=False)

def bus_time_difference ( time_now, due_time ):
    due_time = due_time.replace('T', ' ')[:-1]
    bus_time = datetime.fromisoformat(due_time)
    time_diff = (bus_time - time_now).total_seconds() / 60
    return round(time_diff)

def get_bus():
    client = BusClient()
    client_request = client.get()
    client_json = client_request.json()

    #get utc time, the website responds using UTC
    time_now = datetime.utcnow()

    if client_request.status_code == 200:
        logging.info(client_json)
        sch_bus = []
        for bus in client_json['stopEvents']:
            if 'departureTimeEstimated' in bus:
                sch_bus += [[bus_time_difference(time_now, bus['departureTimePlanned']), 'Live']]
            else:
                sch_bus += [[bus_time_difference(time_now, bus['departureTimePlanned']), '--']]
        logging.info(sch_bus)
        return sch_bus
    logging.error("Error connecting to TransportForIreland.ie!\nError : %s", client_request.status_code)
    return False

if __name__ == '__main__':
    get_bus()
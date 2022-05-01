import logging
import requests
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

def bus_time_difference ( time_now, due_time ):
    due_time = due_time.replace('T', ' ')[:-1]
    bus_time = datetime.fromisoformat(due_time)
    time_diff = (bus_time - time_now).total_seconds() / 60
    return round(time_diff)

def get_bus_url(stop_num):
    base_url = f"https://journeyplanner.transportforireland.ie/nta/XML_DM_REQUEST?language=en&type_dm=stopID&name_dm=8370B{stop_num}&std3_mapDMMacroIBI=true&outputFormat=rapidJSON&coordOutputFormat=WGS84%5Bdd.ddddd%5D"
    return base_url

def get_bus(stop_num):
    client_request = requests.get(get_bus_url(stop_num))
    client_json = client_request.json()

    #get utc time, the website responds using UTC
    time_now = datetime.utcnow()

    if client_request.status_code == 200:
        logging.info(client_json)
        sch_bus = []
        for bus in client_json['stopEvents']:
            time_arrive = bus_time_difference(time_now, bus['departureTimePlanned'])
            if 'departureTimeEstimated' in bus:
                sch_bus += [[time_arrive, 'Live', bus['transportation']['disassembledName']]]
            else:
                sch_bus += [[time_arrive, '--', bus['transportation']['disassembledName']]]
        logging.info(sch_bus)
        return sch_bus
    logging.error("Error connecting to TransportForIreland.ie!\nError : %s", client_request.status_code)
    return False

if __name__ == '__main__':
    get_bus()
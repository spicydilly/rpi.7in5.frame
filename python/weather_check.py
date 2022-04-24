"""
This module uses WeatherAPI to get weather updates
"""
import os
import logging
import requests

logging.basicConfig(level=logging.DEBUG)

class WeatherClient ():
    """Class for api requests to WeatherAPI"""
    BASE_URL = f"https://api.weatherapi.com/v1/current.json?key="\
        f"{os.environ['WEATHER_API_KEY']}&q=Cork&aqi=no"
    HEADERS = {'Content-type': 'application/json'}

    def get(self):
        """Get request"""
        url = f'{self.BASE_URL}'
        return requests.get(url, headers=self.HEADERS)

def get_current (client):
    """
    Checks current weather
    """
    current_request = client.get()
    current_json = current_request.json()
    if current_request.status_code == 200:
        logging.info(current_json)
        return current_json
        
    logging.error("Error connecting to WeatherAPI!\nError : %s", current_request.status_code)
    return False

if __name__ == '__main__':
    weather_client = WeatherClient()
    get_current(weather_client)

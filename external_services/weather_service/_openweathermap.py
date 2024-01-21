import requests
from typing import Union
import ast

from external_services.API_KEYS import OPEN_WEATHER_MAP_API_KEY as API_KEY


# default_include = ('current', 'minutely', 'hourly', 'daily')
# api_include = ('current', 'minutely', 'hourly', 'daily', 'alerts')


# ----- UTILITY ----- #
def _collection_to_string(collection: Union[list, tuple]):  # this function is useless
    ret_str = ''
    for item in collection:
        ret_str += str(item) + ','
    ret_str = ret_str.removesuffix(',')
    return ret_str


# ----- API ----- #
def get_forecast_raw(latitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric"
    return ast.literal_eval(requests.post(url).text)


def get_forecast(latitude: float, longitude: float) -> tuple:
    current_weather = get_forecast_raw(latitude, longitude)
    return current_weather['main']['temp'], current_weather['main']['humidity'], current_weather['weather'][0]['main']


# ----- TEST ----- #

if __name__ == '__main__':
    print(get_forecast_raw(20, 30))
    print(get_forecast(20, 30))

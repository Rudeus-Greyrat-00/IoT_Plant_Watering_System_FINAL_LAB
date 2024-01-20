import requests
from typing import Union

from ..API_KEYS import OPEN_WEATHER_MAP_API_KEY as API_KEY

default_include = ('current', 'minutely', 'hourly', 'daily')
api_include = ('current', 'minutely', 'hourly', 'daily', 'alerts')


# ----- UTILITY ----- #
def _collection_to_string(collection: Union[list, tuple]):
    ret_str = ''
    for item in collection:
        ret_str += str(item) + ','
    ret_str = ret_str.removesuffix(',')
    return ret_str


# ----- API ----- #
def get_forecast(latitude, longitude, include=default_include):
    if include is None or len(include) == 0:
        raise InvalidWeatherSelectionException()
    for include_item in include:
        if include_item not in api_include:
            raise InvalidWeatherSelectionException()

    exclude_list = []
    for api_item in api_include:
        if api_item not in include:
            exclude_list.append(api_item)
    part = _collection_to_string(exclude_list)

    url = f"https://api.openweathermap.org/data/3.0/onecall?lat=" \
          f"{latitude}&lon={longitude}&exclude={part}&appid={API_KEY}"
    return requests.post(url).text


# ----- EXCEPTIONS ---- #

class InvalidWeatherSelectionException(ValueError):
    def __init__(self):
        self.message = 'include parameter must be a list containing at least ' \
                       'one among these elements:' + str(default_include)
        super().__init__(self.message)


# ----- TEST ----- #

if __name__ == '__main__':
    print(get_forecast('10', '10', ['current']))


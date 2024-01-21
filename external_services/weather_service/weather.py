from _openweathermap import get_forecast as gf


# ----- INTERFACES ----- #

class WeatherState:
    def __init__(self, temperature, humidity, weather, longitude, latitude, country):
        self.temperature = temperature
        self.humidity = humidity
        self.weather = weather
        self.longitude = longitude
        self.latitude = latitude
        self.country = country

    def __str__(self):
        return f"Location: coordinates (lat, lon): {self.latitude}, {self.longitude}, " \
               f"Country: {self.country} <---> " \
               f"Weather: {self.weather}, Temperature: {self.temperature}°C, Humidity: {self.humidity}%"


def get_forecast(latitude: float, longitude: float) -> WeatherState:
    weather_dict = gf(latitude=latitude, longitude=longitude)
    return WeatherState(temperature=weather_dict['temperature'], humidity=weather_dict['humidity'],
                        weather=weather_dict['weather'], latitude=weather_dict['longitude'],
                        longitude=weather_dict['latitude'], country=weather_dict['country_code'])


# ------ TEST ------ #

if __name__ == '__main__':
    print(get_forecast(20, 30))

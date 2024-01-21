from _openweathermap import get_forecast as gf


# ----- INTERFACES ----- #

class WeatherState:
    def __init__(self, temperature, humidity, weather):
        self.temperature = temperature
        self.humidity = humidity
        self.weather = weather

    def __str__(self):
        return f"Weather: {self.weather}, Temperature: {self.temperature}°C, Humidity: {self.humidity}%"


def get_forecast(latitude: float, longitude: float) -> WeatherState:
    weather_tuple = gf(latitude=latitude, longitude=longitude)
    return WeatherState(weather_tuple[0], weather_tuple[1], weather_tuple[2])


# ------ TEST ------ #

if __name__ == '__main__':
    print(get_forecast(20, 30))

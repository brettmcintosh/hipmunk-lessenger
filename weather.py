import requests

import secrets
from datastructures import LocationCoords, Weather
from exceptions import WeatherError


def get_weather(coords: LocationCoords, time: str) -> Weather:
    """Get the current weather for a location."""
    url = 'https://api.darksky.net/forecast/{key}/{coords.lat},{coords.long}'.format(
        key=secrets.DARK_SKY_API_KEY,
        coords=coords
    )
    try:
        weather_index = 0
        if time == ' tomorrow':
            time = time.strip()
            weather_index = 1
        else:
            time = 'today'
        weather = requests.get(url).json()
        low_temperature = weather['daily']['data'][weather_index]['temperatureLow']
        high_temperature = weather['daily']['data'][weather_index]['temperatureHigh']
        description = weather['daily']['data'][weather_index]['summary']
    except KeyError:
        # raise WeatherError(
        #     'Could not find weather for: {}'.format(coords),
        #     data=coords
        # )
        raise
    return Weather(
        low_temperature=low_temperature,
        high_temperature=high_temperature,
        description=description,
        time=time)

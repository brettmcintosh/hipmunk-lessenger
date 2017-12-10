import requests

import secrets
from datastructures import LocationCoords, Weather
from exceptions import WeatherError


def get_weather(coords: LocationCoords) -> Weather:
    """Get the current weather for a location."""
    url = 'https://api.darksky.net/forecast/{key}/{coords.lat},{coords.long}'.format(
        key=secrets.DARK_SKY_API_KEY,
        coords=coords
    )
    try:
        weather = requests.get(url).json()
        temperature = weather['currently']['temperature']
        description = weather['currently']['summary']
    except KeyError:
        raise WeatherError(
            'Could not find weather for: {}'.format(coords),
            data=coords
        )
    return Weather(temperature=temperature, description=description)

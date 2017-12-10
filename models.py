import random
import re

from flask import jsonify, render_template_string, Response

import phrases
import templates
from datastructures import LocationCoords, Weather
from exceptions import LocationError, ParseError
from geo import geo_service
from weather import get_weather


class BaseMessage:
    """A chat message from the server to the client."""
    TEMPLATE_CHOICES = ('', )

    def __init__(self, context=None):
        self.context = context
        self.template = random.choice(self.TEMPLATE_CHOICES)
        self.body = None

    def render_body(self):
        """Render a random template."""
        self.body = render_template_string(self.template, **self.context)

    def as_json(self) -> Response:
        """Return a JSON response for the Lessenger UI."""
        self.render_body()
        response = {
            'messages': [
                {
                    'type': 'text',
                    'text': self.body
                }
            ]
        }
        return jsonify(**response)


class Greeting(BaseMessage):
    """A greeting message for the start of a chat session."""
    TEMPLATE_CHOICES = templates.GREETINGS


class WeatherReport(BaseMessage):
    """A message that gives a forecast for a location."""
    TEMPLATE_CHOICES = templates.WEATHER_REPORTS

    def __init__(self, context=None):
        self.phrase_regex = tuple(
            re.compile(pattern)
            for pattern in phrases.QUERY_PHRASES
        )
        super().__init__(context=context)

    def render_body(self):
        parsed_location = self.parse_location(self.context)
        location = self.get_location(parsed_location)
        forecast = self.get_current_weather(location)
        self.context = forecast.as_dict()
        super().render_body()

    def parse_location(self, form_body: dict) -> str:
        """Parse the query and extract the location string."""
        query = form_body['text']
        for regex in self.phrase_regex:
            result = regex.match(query)
            if result is not None:
                return result.group(1)
        raise ParseError(
            'Did not recognize phrase: {}'.format(query),
            data=query
        )

    def get_location(self, parsed_location: str) -> LocationCoords:
        """Fetch location from geo service."""
        location_results = geo_service.geocode(parsed_location)
        if len(location_results) == 0:
            raise LocationError(
                'Unable to find location: {}'.format(parsed_location),
                data=parsed_location
            )
        first_result_coords = location_results[0]['geometry']['location']
        coords = first_result_coords['lat'], first_result_coords['lng']
        return LocationCoords(*coords)

    def get_current_weather(self, location: LocationCoords) -> Weather:
        """Fetch forecast from weather API."""
        return get_weather(location)


class ParseErrorMessage(BaseMessage):
    """A message for a query that can't be parsed."""
    TEMPLATE_CHOICES = templates.PARSE_ERROR


class LocationErrorMessage(BaseMessage):
    """A message for a location that can't be resolved."""
    TEMPLATE_CHOICES = templates.LOCATION_ERROR


class WeatherErrorMessage(BaseMessage):
    """A message for a location with no weather results."""
    TEMPLATE_CHOICES = templates.WEATHER_ERROR

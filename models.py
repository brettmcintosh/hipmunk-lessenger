import random
from typing import NamedTuple

from flask import jsonify, render_template_string

import templates


class LocationCoords(NamedTuple):
    """The latitude and longitude coordinates of a location."""
    lat: str
    long: str


class BaseMessage:
    """A chat message from the server to the client."""

    TEMPLATE_CHOICES = ('', )

    def __init__(self, form_body):
        self.context = form_body
        self.template = random.choice(self.TEMPLATE_CHOICES)
        self.body = self.render_body()

    def render_body(self) -> str:
        return render_template_string(self.template, **self.context)

    def as_json(self) -> str:
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


class Forecast(BaseMessage):
    """A message that gives a forecast for a location."""

    TEMPLATE_CHOICES = templates.FORECASTS

    def __init__(self, form_body):
        parsed_location = self.parse_location(form_body)
        location = self.get_location(parsed_location)
        forecast = self.get_forecast(location)
        super().__init__(forecast)

    def parse_location(self, form_body: dict) -> str:
        return ''

    def get_location(self, parsed_location: str) -> LocationCoords:
        # Fetch location from geo API
        return LocationCoords('', '')

    def get_forecast(self, location: LocationCoords) -> dict:
        # Fetch forecast from weather API
        return {
            'temperature': '30',
            'description': 'sunny',
        }

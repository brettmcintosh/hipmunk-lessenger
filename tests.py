import json
import unittest
from unittest.mock import Mock, patch

import requests
from flask import Response

from app import app as main_app
from datastructures import LocationCoords
from exceptions import LocationError, ParseError, WeatherError
from models import BaseMessage, WeatherReport
from weather import get_weather


class ChatTestCase(unittest.TestCase):

    def setUp(self):
        main_app.testing = True
        self.app_context = main_app.test_request_context('/chat/messages')


class TestBaseMessage(ChatTestCase):

    def setUp(self):
        super().setUp()
        BaseMessage.TEMPLATE_CHOICES = ('{{ name }}', )

    def test_render_body(self):
        """Test that template is rendered with the context."""
        with self.app_context:
            self.msg = BaseMessage({'name': 'test_name'})
            self.msg.render_body()
            self.assertEqual(self.msg.body, 'test_name')

    def test_as_json(self):
        """Test that as_json returns the correct format."""
        with self.app_context:
            self.msg = BaseMessage({'name': 'test_name'})
            self.assertEqual(
                json.loads(self.msg.as_json().data),
                {
                    'messages': [
                        {
                            'type': 'text',
                            'text': 'test_name'
                        }
                    ]
                }
            )


class TestWeatherReport(ChatTestCase):

    def setUp(self):
        super().setUp()
        WeatherReport.TEMPLATE_CHOICES = ('{{ temperature }} - {{ description }}', )
        self.test_phrases = (
            'what\'s the weather in San Francisco',
            'weather in San Francisco',
            'San Francisco weather',
        )

    def test_parse_location(self):
        """Test that parse_location extracts the query string."""
        with self.app_context:
            for phrase in self.test_phrases:
                report = WeatherReport()
                self.assertEqual(
                    report.parse_location({'text': phrase}),
                    'San Francisco'
                )

    def test_parse_location_exception(self):
        """Test that parse location raises ParseError on bad input."""
        with self.app_context:
            report = WeatherReport()
            with self.assertRaises(ParseError):
                report.parse_location({'text': 'asdf'})

    @patch('models.geo_service.geocode')
    def test_get_location(self, geocode_mock: Mock):
        """
        Test that get_location passes the query string to geo_service
        and returns LocationCoords.
        """
        geocode_mock.return_value = [{
            'geometry': {
                'location': {
                    'lat': 100,
                    'lng': 200,
                }
            }
        }]
        with self.app_context:
            report = WeatherReport()
            location = report.get_location('San Francisco')
            geocode_mock.assert_called_once_with('San Francisco')
            self.assertEqual(
                location,
                LocationCoords(lat=100, long=200)
            )

    @patch('models.geo_service.geocode')
    def test_get_location_exception(self, geocode_mock: Mock):
        """
        Test that get_location raises LocationError when no geo_service results.
        """
        geocode_mock.return_value = []
        with self.app_context:
            report = WeatherReport()
            with self.assertRaises(LocationError):
                report.get_location('San Francisco')

    @patch('models.get_weather')
    def test_get_current_weather(self, get_weather_mock: Mock):
        """Test that get_current_weather calls get_weather."""
        with self.app_context:
            report = WeatherReport()
            location = LocationCoords(lat=100, long=200)
            report.get_current_weather(location)
            get_weather_mock.assert_called_once_with(location)

    @patch('weather.requests.get')
    def test_get_weather(self, requests_get_mock: Mock):
        """Test that get_weather makes a GET request."""
        with self.app_context:
            location = LocationCoords(lat=100, long=200)
            get_weather(location)
            requests_get_mock.assert_called_once()

    @patch('weather.requests.Response.json')
    @patch('weather.requests.get')
    def test_get_weather_exception(self, get_mock: Mock, json_mock: Mock):
        """Test that get_weather raises WeatherError when no weather results."""
        get_mock.return_value = requests.Response()
        json_mock.return_value = {}
        with self.app_context:
            location = LocationCoords(lat=100, long=200)
            with self.assertRaises(WeatherError):
                get_weather(location)


class AppTestCase(ChatTestCase):

    def setUp(self):
        super().setUp()
        self.test_client = main_app.test_client()
        self.data = {
            'action': 'message',
            'text': 'test_text'
        }

    def test_bad_request(self):
        """Malformed data should return 400."""
        response = self.test_client.post(
            '/chat/messages',
            data={'bad': 'data'}
        )
        self.assertEqual(response.status_code, 400)

    @patch('app.Greeting.as_json')
    def test_dispatch_greeting(self, as_json_mock: Mock):
        """A join message should return a Greeting."""
        as_json_mock.return_value = Response()
        self.test_client.post(
            '/chat/messages',
            data={
                'action': 'join',
                'name': 'test_name'
            }
        )
        as_json_mock.assert_called_once()

    @patch('app.WeatherReport.as_json')
    def test_dispatch_weather_report(self, as_json_mock: Mock):
        """A normal message should return a WeatherReport."""
        as_json_mock.return_value = Response()
        self.test_client.post('/chat/messages', data=self.data)
        as_json_mock.assert_called_once()

    @patch('app.WeatherReport.parse_location')
    @patch('app.ParseErrorMessage.as_json')
    def test_dispatch_parse_error(self, as_json_mock: Mock, parse_location_mock: Mock):
        """A parsing error will return a ParseErrorMessage."""
        parse_location_mock.side_effect = ParseError('')
        as_json_mock.return_value = Response()
        self.test_client.post('/chat/messages', data=self.data)
        as_json_mock.assert_called_once()

    @patch('app.WeatherReport.get_location')
    @patch('app.WeatherReport.parse_location')
    @patch('app.LocationErrorMessage.as_json')
    def test_dispatch_location_error(self, as_json_mock: Mock, parse_location_mock: Mock,
                                     get_location_mock: Mock):
        """A location error will return a LocationErrorMessage."""
        parse_location_mock.return_value = 'test_location'
        get_location_mock.side_effect = LocationError('')
        as_json_mock.return_value = Response()
        self.test_client.post('/chat/messages', data=self.data)
        as_json_mock.assert_called_once()

    @patch('app.WeatherReport.get_current_weather')
    @patch('app.WeatherReport.get_location')
    @patch('app.WeatherReport.parse_location')
    @patch('app.WeatherErrorMessage.as_json')
    def test_dispatch_weather_error(self, as_json_mock: Mock, parse_location_mock: Mock,
                                     get_location_mock: Mock, weather_mock: Mock):
        """A weather error will return a WeatherErrorMessage."""
        parse_location_mock.return_value = 'test_location'
        get_location_mock.return_value = LocationCoords(lat=100, long=200)
        weather_mock.side_effect = WeatherError('')
        as_json_mock.return_value = Response()
        self.test_client.post('/chat/messages', data=self.data)
        as_json_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()

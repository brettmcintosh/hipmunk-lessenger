from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from exceptions import LocationError, ParseError, WeatherError
from models import (
    WeatherReport, Greeting, LocationErrorMessage, ParseErrorMessage,
    WeatherErrorMessage
)

app = Flask(__name__)
CORS(app, resources={r'/chat/messages': {'origins': 'http://hipmunk.github.io'}})


@app.route('/chat/messages', methods=('POST', ))
def dispatch():
    form_action = request.form.get('action')
    if form_action == 'join' and 'name' in request.form:
        return Greeting(request.form.to_dict()).as_json()
    elif form_action == 'message' and 'text' in request.form:
        try:
            return WeatherReport(request.form.to_dict()).as_json()
        except ParseError as e:
            return ParseErrorMessage(e.get_context()).as_json()
        except LocationError as e:
            return LocationErrorMessage(e.get_context()).as_json()
        except WeatherError as e:
            return WeatherErrorMessage(e.get_context()).as_json()
    raise BadRequest()


if __name__ == '__main__':
    app.run(port=9000)

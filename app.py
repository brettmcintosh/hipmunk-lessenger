from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest

from models import Greeting, Forecast

app = Flask(__name__)
CORS(app, resources={r'/chat/messages': {'origins': 'http://hipmunk.github.io'}})


@app.route('/chat/messages', methods=('POST', ))
def dispatch():
    form_action = request.form.get('action')
    if form_action == 'join' and 'name' in request.form:
        return Greeting(request.form.to_dict()).as_json()
    elif form_action == 'message' and 'text' in request.form:
        return Forecast(request.form.to_dict()).as_json()
    raise BadRequest


if __name__ == '__main__':
    app.run(debug=True, port=9000)

from flask import Flask
import flask
from markovgen import Markov
import requests
import json
import os

with open('filtrado.txt') as corpus:
    m = Markov(corpus)

app = Flask(__name__)

token = os.environ.get("TELEGRAM_BOT_TOKEN")
api_url = "https://api.telegram.org/bot{}/sendMessage".format(token)


@app.route('/', methods=['GET', 'POST'])
def harry():
    import urllib
    if flask.request.method == 'GET':
        return m.generate_markov_text()
    params = dict()
    data = flask.request.get_json()
    message = data['message']
    if '/harry' in message["text"]:

        s = m.generate_markov_text()
        params = {
            'chat_id': message['chat']['id'],
            # por algun motivo los \n no se encodean
            'text': s.strip(),
        }
        requests.get(api_url, params=params)
    return json.dumps(params)

if __name__ == "__main__":
    app.run()

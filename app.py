from flask import Flask
import flask
from markovgen import Markov
import requests
import json

with open('corpus.txt') as corpus:
    m = Markov(corpus)

app = Flask(__name__)

token = "376658113:AAHh2TcsvcuKAFwYuBeQwCfSLUBUQm2Dfms"
api_url = "https://api.telegram.org/bot{}/sendMessage".format(token)


@app.route('/')
def harry():
    data = flask.request.get_json()
    if not data:
        return m.generate_markov_text()
    params = dict()
    if "message" in data and "/harry" in data["message"]["text"]:
        s = m.generate_markov_text()
        params = {
            'chat_id': data['message']['chat']['id'],
            'text': s,
        }
        requests.get(api_url, params=params)
    return json.dumps(params)

if __name__ == "__main__":
    app.run()

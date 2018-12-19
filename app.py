from flask import Flask
import flask
from markovgen import Markov
import requests
import json
import os
import random


app = Flask(__name__)

token = os.environ.get("TELEGRAM_BOT_TOKEN")
api_url = "https://api.telegram.org/bot{}/sendMessage".format(token)

sal = [
    "el pico",
    "la sal",
    "la disonancia cognitiva",
    "la concha",
    "el pene",
    "chilezuela",
    "la concerta",
    "anos",
]


@app.route('/', methods=['GET', 'POST'])
def harry():
    with open('filtrado.txt') as corpus:
        m = Markov(corpus)
    import urllib
    if flask.request.method == 'GET':
        return m.generate_markov_text()
    params = dict()
    data = flask.request.get_json()
    try:
        message = data['message']
        params = dict(
            chat_id=message['chat']['id'],
        )
        if '/harry' in message["text"]:
            params['text'] = "jan culiao chupa " + random.choice(sal),
        elif '/echo' in message["text"]:
            params['text'] = json.dumps(
                message,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
        requests.get(api_url, params=params)

    except:
        flask.abort(400)
    return json.dumps(
        params,
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )


@app.route('/notify/<chat_id>/<texto>', methods=['GET'])
def notification(chat_id, texto):
    """
    /notify envia una notificacion al chat_id
    """
    if chat_id == "me":
        chat_id = os.environ.get("MY_CHAT_ID")
    params = dict(
        chat_id=chat_id,
        text=texto
    )

    r = requests.get(api_url, params=params)
    return json.dumps(
        params, sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )

if __name__ == "__main__":
    app.run()

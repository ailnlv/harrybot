from flask import Flask
import flask
from markovgen import Markov
import requests

with open('corpus.txt') as corpus:
    m = Markov(corpus)

app = Flask(__name__)

token = "376658113:AAHh2TcsvcuKAFwYuBeQwCfSLUBUQm2Dfms"
api_url = "https://api.telegram.org/bot{}/sendMessage".format(token)


@app.route('/echo')
def echo():
    return str(request)


@app.route('/')
def harry():
    s = m.generate_markov_text()
    message = flask.request.args.get('message')
    if message and "/harry" in message.text:
        message = dict(chat=dict(id=12700726), text='/harry')

    return s

if __name__ == "__main__":
    app.run()

from flask import Flask
from markovgen import Markov
import requests

with open('corpus.txt') as corpus:
    m = Markov(corpus)

app = Flask(__name__)

token = "376658113:AAHh2TcsvcuKAFwYuBeQwCfSLUBUQm2Dfms"
api_url = "https://api.telegram.org/bot{}/sendMessage".format(token)


@app.route('/')
def hello_world():
    return m.generate_markov_text()

if __name__ == "__main__":
    app.run()

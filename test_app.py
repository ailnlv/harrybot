import pytest
import sys
import requests
import json


req = dict()


@pytest.fixture(autouse=True)
def no_requests(monkeypatch):
    """
    El request devuelve el json estandar. Los argumentos del request
    se guardan en req
    """
    def fake_req(url, **params):
        global req
        req = dict(
            url=url,
            params=params['params'],
        )
        return {
            "ok": True,
            "result":            {
                "message_id": 65,
                "from": {
                    "id": 376658113,
                    "first_name": "HarryBot",
                    "username": "elbb_bot"
                },
                "chat": {
                    "id": 12700726,
                    "first_name": "Andr\u00e9s",
                    "last_name": "Letelier",
                    "username": "letelier",
                    "type": "private"},
                "date": 1494187142,
                "text": "hola"}}
    monkeypatch.setattr(requests, "get", fake_req)


@pytest.fixture()
def app():
    import app
    return app.app


@pytest.fixture()
def json_data():
    headers = [('Content-Type', 'application/json')]
    data = {
        "update_id": 10000,
        "message": {
            "date": 1441645532,
            "chat": {
                "last_name": "Test Lastname",
                "id": 1111111,
                "first_name": "Test",
                "username": "Test"
            },
            "message_id": 1365,
            "from": {
                "last_name": "Test Lastname",
                "id": 1111111,
                "first_name": "Test",
                "username": "Test"
            },
            "text": "/harry"
        }
    }
    return dict(headers=headers, data=data)


def test_harry(client, json_data):
    """
    Insulto gratuito con cadenas de markov
    """
    r = client.post('/', data=json.dumps(json_data["data"]), headers=json_data["headers"])
    assert r.status == '200 OK'
    return_data = json.loads(r.data)
    assert all(x in return_data for x in ['text', 'chat_id'])
    assert return_data['chat_id'] == json_data['data']['message']['chat']['id']


def test_harry_sin_comando(client, json_data):
    headers = [('Content-Type', 'application/json')]
    json_data['data']['message']['text'] = '/asdf'
    r = client.post('/', data=json.dumps(json_data["data"]), headers=json_data["headers"])
    assert r.status == '200 OK'
    return_data = json.loads(r.data)
    assert return_data == {}


def test_harry_get(client):
    r = client.get('/')
    assert r.status == '200 OK'


def test_request(client, json_data, monkeypatch):
    """
    Probando que el request se haga correctamente
    """
    global req
    from re import match
    from markovgen import Markov
    monkeypatch.setattr(Markov, 'generate_markov_text', lambda _: "hola\nchao")

    r = client.post('/', headers=json_data['headers'], data=json.dumps(json_data['data']))
    assert match('https://api.telegram.org/bot.*/sendMessage',
                 req["url"]), "La url tiene que apuntar a la api de telegram"
    assert req['params']['text'] == "hola\nchao", "El texto tiene que venir url-encoded"


def test_harry_methods(client, json_data):
    """
    Harry tiene que responder por get y post
    """
    r = client.get('/', headers=json_data['headers'], data=json.dumps(json_data['data']))
    assert r.status == '200 OK', "Tiene que responder GET"
    r = client.post('/', headers=json_data['headers'], data=json.dumps(json_data['data']))
    assert r.status == '200 OK', "Tiene que responder POST"

if __name__ == '__main__':
    pytest.main()

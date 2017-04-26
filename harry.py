import random
import requests

token = "376658113:AAHh2TcsvcuKAFwYuBeQwCfSLUBUQm2Dfms"
api_url = "https://api.telegram.org/bot{}/sendMessage".format(token)
mensajes = [
    "chupa el pico",
    "aweonao",
    "ojala te mueras",
    "jan culiao te amo",
  ]

s = random.choice(mensajes)

if 'message' not in Hook['params']:
    Hook['params']['message']=dict(chat=dict(id=12700726), text='/harry')

if '/harry' in Hook['params']['message']['text']:    
    requests.get(api_url, params={
        'chat_id': Hook['params']['message']['chat']['id'],
        'text': s,
    }, verify=False)

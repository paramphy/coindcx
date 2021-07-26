import os
import hmac
import hashlib
import base64
import json
import time
import requests
from coindcxfunctions import *
from keep_alive import keep_alive

# Enter your API Key and Secret here. If you don't have one, you can generate it from CoinDCX website.
key = os.environ['key']

secret = os.environ['secret']

# python3
secret_bytes = bytes(secret, encoding='utf-8')


keep_alive()
while True:

  coinname = 'ETCINR'

  buy_coin_if_low(coinname, 3500, 0.1,key, secret)

  time.sleep(2*60)

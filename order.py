import os
import hmac
import hashlib
import base64
import json
import time
import requests

# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.

key = os.environ['key']

secret = os.environ['secret']

# python3
secret_bytes = bytes(secret, encoding='utf-8')

# Generating a timestamp.
timeStamp = int(round(time.time() * 1000))

body = {
  "side": "buy",    #Toggle between 'buy' or 'sell'.
  "order_type": "market_order", #Toggle between a 'market_order' or 'limit_order'.
  "market": "DOGEINR", #Replace 'SNTBTC' with your desired market pair.
  #"price_per_unit": 17, #This parameter is only required for a 'limit_order'
  "total_quantity": 5, #Replace this with the quantity you want
  "timestamp": timeStamp
}

json_body = json.dumps(body, separators = (',', ':'))

signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

url = "https://api.coindcx.com/exchange/v1/orders/create"

headers = {
    'Content-Type': 'application/json',
    'X-AUTH-APIKEY': key,
    'X-AUTH-SIGNATURE': signature
}

response = requests.post(url, data = json_body, headers = headers)
data = response.json()
print(data)



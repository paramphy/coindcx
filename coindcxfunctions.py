import os
import hmac
import hashlib
import base64
import json
import time
import requests

# Enter your API Key and Secret here. If you don't have one, you can generate it from CoinDCX website.
key = os.environ['key']

secret = os.environ['secret']

# python3
secret_bytes = bytes(secret, encoding='utf-8')

def cancle_order(id):

  # Generating a timestamp.
  timeStamp = int(round(time.time() * 1000))

  body = {
      "id": id, # Enter your Order ID here.
      "timestamp": timeStamp
  }

  json_body = json.dumps(body, separators = (',', ':'))

  signature = hmac.new(secret_bytes, json_body.encode(),  hashlib.sha256).hexdigest()

  url = "https://api.coindcx.com/exchange/v1/orders/cancel"

  headers = {
      'Content-Type': 'application/json',
      'X-AUTH-APIKEY': key,
      'X-AUTH-SIGNATURE': signature
  }

  response = requests.post(url, data = json_body, headers = headers)
  data = response.json()
  print(data)

def buy_market_order(coinpair, amount, key, secret):
  timeStamp = int(round(time.time() * 1000))

  body = {
    "side": "buy",    #Toggle between 'buy' or 'sell'.
    "order_type": "market_order", #Toggle between a 'market_order'  or 'limit_order'.
    "market": coinpair, #Replace 'SNTBTC' with your desired market   pair.
    #"price_per_unit": 17, #This parameter is only required for a   'limit_order'
    "total_quantity": amount, #Replace this with the quantity you want
    "timestamp": timeStamp
  }

  json_body = json.dumps(body, separators = (',', ':'))

  signature = hmac.new(secret_bytes, json_body.encode(),  hashlib.sha256).hexdigest()

  url = "https://api.coindcx.com/exchange/v1/orders/create"

  headers = {
      'Content-Type': 'application/json',
      'X-AUTH-APIKEY': key,
      'X-AUTH-SIGNATURE': signature
  }

  response = requests.post(url, data = json_body, headers = headers)
  data = response.json()
  print(data)

def sell_market_order(coinpair, amount, key, secret):
     
  timeStamp = int(round(time.time() * 1000))

  body = {
    "side": "sell",    #Toggle between 'buy' or 'sell'.
    "order_type": "market_order", #Toggle between a 'market_order'  or 'limit_order'.
    "market": coinpair, #Replace 'SNTBTC' with your desired market   pair.
    #"price_per_unit": 17, #This parameter is only required for a   'limit_order'
    "total_quantity": amount, #Replace this with the quantity you want
    "timestamp": timeStamp
    }

  json_body = json.dumps(body, separators = (',', ':'))

  signature = hmac.new(secret_bytes, json_body.encode(),  hashlib.sha256).hexdigest()

  url = "https://api.coindcx.com/exchange/v1/orders/create"

  headers = {
      'Content-Type': 'application/json',
      'X-AUTH-APIKEY': key,
      'X-AUTH-SIGNATURE': signature
  }

  response = requests.post(url, data = json_body, headers = headers)
  data = response.json()
  print(data)
  return(data)

def my_balance(key, secret):
    # Generating a timestamp
  timeStamp = int(round(time.time() * 1000))
  
  body = {
      "timestamp": timeStamp
  }
  
  json_body = json.dumps(body, separators = (',', ':'))
  
  signature = hmac.new(secret_bytes, json_body.encode(),  hashlib.sha256).hexdigest()
  
  url = "https://api.coindcx.com/exchange/v1/users/balances"
  
  headers = {
      'Content-Type': 'application/json',
      'X-AUTH-APIKEY': key,
      'X-AUTH-SIGNATURE': signature
  }
  
  response = requests.post(url, data = json_body, headers = headers)
  data = response.json();
  return(data)

def ticker(coiname):

  url = "https://api.coindcx.com/exchange/ticker"

  response = requests.get(url)
  data = response.json()

  for item in data:

    if item['market'] == coiname:
      return(item)

def buy_coin_if_low(coinname, buy_price, coin_amount,key, secret):

  coindata = ticker(coinname)
  print(coindata)
  balance = my_balance(key,secret)

  for item in balance:

    if item['currency'] == 'INR':

      inr_balance = float(item['balance'])

  if inr_balance>3000:

    print('INR Balance',inr_balance)

    if float(coindata['last_price']) < buy_price:
    
      if coindata['last_price']*coin_amount < 200:
      
        buy_market_order(coindata['market'], coin_amount, key, secret)
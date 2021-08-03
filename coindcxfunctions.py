import os
import hmac
import hashlib
import base64
import json
import time
import requests
from tqdm import tqdm

# Enter your API Key and Secret here. If you don't have one, you can generate it from CoinDCX website.
key = os.environ['key']

secret = os.environ['secret']

# python3
secret_bytes = bytes(secret, encoding='utf-8')

def send_mail(coin_name, coin_price, coin_amount):
  from mailjet_rest import Client
  api_key = os.environ['MAILJET_API_KEY']
  
  api_secret = os.environ['MAILJET_API_SECRET']
  
  mailjet = Client(auth=(api_key, api_secret), version='v3.1')
  data = {
    'Messages': [
      {
        "From": {
          "Email": "nanoscskm@gmail.com"
  
  ,
          "Name": "Paramesh"
        },
        "To": [
          {
            "Email": "parameshchandra28@gmail.com",
            "Name": "Paramesh"
          }
        ],
        "Subject": "Notification from CoinDCX bot",
        "TextPart": coin_name + " is sold." + 'Price when sold ' + str(coin_amount) + '. Amount sold: ' + str(coin_amount),
        
        "CustomID": "AppGettingStartedTest"
      }
    ]
  }
  result = mailjet.send.create(data=data)
  if result.status_code == 200:
    print('Your mail is sucessfully sent.')

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

def buy_limit_order(coinpair, amount, key, secret,unitprice):

  timeStamp = int(round(time.time() * 1000))

  body = {
    "side": "buy",    #Toggle between 'buy' or 'sell'.
    "order_type": "limit_order", #Toggle between a 'market_order'  or 'limit_order'.
    "market": coinpair, #Replace 'SNTBTC' with your desired market   pair.
    "price_per_unit": unitprice, #This parameter is only required for a   'limit_order'
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

def sell_limit_order(coinpair, amount,coinprice, key, secret,unitprice):
     
  timeStamp = int(round(time.time() * 1000))

  body = {
    "side": "sell",    #Toggle between 'buy' or 'sell'.
    "order_type": 'limit_order', #Toggle between a 'market_order'  or 'limit_order'.
    "market": coinpair, #Replace 'SNTBTC' with your desired market   pair.
    "price_per_unit": unitprice, #This parameter is only required for a   'limit_order'
    "total_quantity": coinprice*amount/100, #Replace this with the quantity you want
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

  coindata, status = coin_price_and_status(coinname)
  print('Last Pice: ',coindata['last_price'])
  coinprice = coindata['last_price']
  balance = my_balance(key,secret)

  for item in balance:

    if item['currency'] == 'INR':

      inr_balance = float(item['balance'])
      print('INR Balance:',inr_balance)
    
    if item['currency'] == 'ETC':

      coin_balance = float(item['balance'])
      print('ETC Balance:',coin_balance)

  if inr_balance>3000:

    if float(coindata['last_price']) < buy_price:
    
      if float(coindata['last_price'])*coin_amount/100 < 500:
      
        buy_limit_order(coindata['market'], coin_amount,coinprice, key, secret)
        print('Crypto is bought')
        send_mail(coinname,coindata['last_price'], coindata['last_price']*coin_amount)

  print('-----------------------------------------------')

  #for n in tqdm (range (30), desc="Waiting...",position=0, leave=True):
  time.sleep(30)

def sell_coin_if_high(coinname, main_coin,sell_price, coin_amount,key, secret):

  coindata, status = coin_price_and_status(coinname)
  print(coindata['market'],'last price: ',coindata['last_price'])
  print(coindata['market'],'desired price to sell: ', sell_price)
  balance = my_balance(key,secret)

  for item in balance:

    if item['currency'] == 'INR':

      inr_balance = float(item['balance'])
      print('INR Balance:',inr_balance)
    
    if item['currency'] == 'USDT':

      inr_balance = float(item['balance'])
      print('USDT Balance:',inr_balance)

    if item['currency'] == main_coin:

      main_coin_balance = float(item['balance'])
      print(main_coin,' Balance:',main_coin_balance)

  balance = main_coin_balance
  
  if main_coin_balance>0.01:


    if float(coindata['last_price']) > sell_price:

      if float(coindata['last_price'])*coin_amount < 500:

        sell_limit_order(coindata['market'], coin_amount, main_coin_balance, key,  secret, coindata['last_price'])
        print('Crypto is sold')
        send_mail(coinname,coindata['last_price'], coindata['last_price']*coin_amount)

  print('-----------------------------------------------')

  #for n in tqdm (range (30), desc="Waiting...",position=0, leave=True):
  time.sleep(30)


def coin_price_and_status(coinname):

  coindata = ticker(coinname)
  old_coinprice = coindata['last_price']
  #for n in tqdm (range (30), desc="Getting price status..."):
  time.sleep(30)
  coindata = ticker(coinname)
  latest_coinprice = coindata['last_price']

  if latest_coinprice < old_coinprice:
    print('Coin value is going down')
    return(coindata,'down')
  elif latest_coinprice > old_coinprice:
    print('Coin value is going up')
    return(coindata,'up')
  elif latest_coinprice == old_coinprice:
    print('Coin value is unchanged') 
    return(coindata,'same')
  
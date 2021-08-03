import os
import hmac
import hashlib
import base64
import json
import time
import requests
from tqdm import tqdm
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
  main_coin = 'ETC'

  buy_coin_if_low(coinname, 3500, 20,key, secret)
  sell_coin_if_high(coinname,main_coin,4000,50, key, secret)

  coinname = 'DASHUSDT'
  main_coin = 'DASH'
#
  #buy_coin_if_low(coinname, 40, 10,key, secret)
  sell_coin_if_high(coinname,main_coin, 160,50, key, secret)

  coinname = 'EOSINR'
  main_coin = 'EOS'
  #buy_coin_if_low(coinname, 3500, 0.1,key, secret)
  sell_coin_if_high(coinname,main_coin,340,50, key, secret)
#
  #buy_coin_if_low(coinname, 3500, 0.1,key, secret)
  #sell_coin_if_high(coinname,4000,0.1, key, secret)

  #for n in tqdm (range (5*60), desc="Sleeping...",position=0, leave=False):
  coinname = 'COMPUSDT'
  main_coin = 'COMP'
  #buy_coin_if_low(coinname, 3500, 0.1,key, secret)
  sell_coin_if_high(coinname,main_coin,420,80, key, secret)
  print('Waiting 5 minutes...')
  time.sleep(5*60)
  

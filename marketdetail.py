import requests # Install requests module first.

def ticker(coiname):

  url = "https://api.coindcx.com/exchange/ticker"

  response = requests.get(url)
  data = response.json()

  coin = {}

  print(data)

  for item in data:

    #if item['market'] == coiname:
    print(item['market'])
    #return(item)
    


coinname = 'ETCINR'
coin = ticker(coinname)
print(coin)

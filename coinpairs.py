import requests # Install requests module first.

url = "https://api.coindcx.com/exchange/v1/markets"

response = requests.get(url)
data = response.json()
for items in data:
  print(items)

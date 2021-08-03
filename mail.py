import os

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

send_mail('ahsh',545,555)

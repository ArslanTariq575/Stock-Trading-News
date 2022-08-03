import requests
from twilio.rest import Client

account_sid = "YOUR SID"
auth_token = "YOUR TOKEN"
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
API_KEY ="YOUR API KEY"
NEWS_API_KEY = "YOUR NEWS_API_KEY"

paramters ={
    "function": "TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":API_KEY,
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#Getting the data
response = requests.get(STOCK_ENDPOINT,params=paramters)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]

#Getting the values and differences
data_list =[value for(key,value) in data.items()]
yesterday_day = float(data_list[0]["4. close"])
day_yesterday = float(data_list[1]["4. close"])
difference = (yesterday_day-day_yesterday)
difference_percent = round((difference/yesterday_day)*(100))

up_down = None
if difference>0:
    up_down = "🔺"
else:
    up_down = "🔻"


news_parm = {
    "apiKey": NEWS_API_KEY,
    "qInTitle":COMPANY_NAME,
}

if difference_percent >=5:
    news_respone = requests.get(NEWS_ENDPOINT,params=news_parm)
    news_respone.raise_for_status()
    articles = news_respone.json()["articles"]
    three_articles = articles[:3]
    format_article = [f"{STOCK_NAME}: {up_down}{difference_percent}%\nHeadLine: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    
    client = Client(account_sid, auth_token)
    for article in format_article:
        message = client.messages.create(
            body=article,
            from_="+18645239947",
            to= "Your_Number"
        )
        print(message.sid)
    



import fillDatabase  as db
import application as app

#db.createTables()
app.menu()




# import time
# import datetime
# import requests
# import json


# def getDateFrom():
#   FROM = datetime.date.today() - datetime.timedelta(365)
#   return int(time.mktime(FROM.timetuple()))

# def getDateTo():
#   TO = datetime.date.today()
#   return int(time.mktime(TO.timetuple()))

# symbol='AAPL'
# FROM = str(getDateFrom())
# print(FROM)
# TO = str(getDateTo())
# print(TO)

# url = 'https://finnhub.io/api/v1/forex/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
# content = requests.get(url).content
# dataset = json.loads(content)
# print(len(dataset['c']))

# url ='https://finnhub.io/api/v1/stock/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
# content = requests.get(url).content
# dataset = json.loads(content)
# print(len(dataset['c']))



       
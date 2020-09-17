import requests
import json
import sqlite3
import time
import datetime
import pandas as pd
import constants as c

def getDateFrom():
  FROM = datetime.date.today() - datetime.timedelta(365)
  return int(time.mktime(FROM.timetuple()))

def getDateTo():
  TO = datetime.date.today()
  return int(time.mktime(TO.timetuple()))


def createStockAnagraphicDataTable():

  stockAnagraphicDataList = list()
  for symbol in c.stockSymbols:
    url ='https://finnhub.io/api/v1/stock/profile2?symbol='+symbol+'&token=btg5t0f48v6r32agadkg'
    content = requests.get(url).content
    dataset = json.loads(content)
    stockAnagraphicDataList.append(dataset.values())

  dataframe = pd.DataFrame(data=stockAnagraphicDataList, columns = dataset.keys())
  connection = sqlite3.connect('database.db')
  dataframe.to_sql('stockAnagraphicData', connection, if_exists='replace', index=False)
  connection.close()


def createStockHistoricalDataTable():
  FROM = str(getDateFrom())
  TO = str(getDateTo())
  stockHistoricalDataList = list()

  for symbol in c.stockSymbols:
    url ='https://finnhub.io/api/v1/stock/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
    content = requests.get(url).content
    dataset = json.loads(content)
    print('dentro lungh di stock')
    print(len(dataset['c']))
    stockHistoricalDataList.append(dataset['c'])

  dataframe = pd.DataFrame(data=stockHistoricalDataList, index = c.stockSymbols)
  dataframeTrasposed = dataframe.transpose()
  connection = sqlite3.connect('database.db')
  dataframeTrasposed.to_sql('stockHistoricalData', connection, if_exists='replace', index=False)
  connection.close()


def createExchangeRatesHistoricalDataTable():
  FROM = str(getDateFrom())
  TO = str(getDateTo())
  exchangeRatesHistoricalDataList = list()

  for symbol in c.exchangeSymbols:
    url = 'https://finnhub.io/api/v1/forex/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
    content = requests.get(url).content
    dataset = json.loads(content)
    print('dentro lungh di exchange')
    print(len(dataset['c']))
    exchangeRatesHistoricalDataList.append(dataset['c'])
  
  dataframe = pd.DataFrame(data=exchangeRatesHistoricalDataList, index = c.exchanges)
  dataframeTrasposed = dataframe.transpose()
  connection = sqlite3.connect('database.db')
  dataframeTrasposed.to_sql('exchangeRatesHistoricalData', connection, if_exists='replace', index=False)
  connection.close()


def createTables():
  createStockAnagraphicDataTable()
  createStockHistoricalDataTable()
  createExchangeRatesHistoricalDataTable()
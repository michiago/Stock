import constants as c
import utils as u

import time
import datetime
import pandas as pd


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
    dataset = u.getDataFromApi(url)
    stockAnagraphicDataList.append(dataset.values())

  dataframe = pd.DataFrame(data=stockAnagraphicDataList, columns = dataset.keys())
  u.insertInDB(dataframe, 'stockAnagraphicData')



def createStockHistoricalDataTable():
  FROM = str(getDateFrom())
  TO = str(getDateTo())
  stockHistoricalDataList = list()

  for symbol in c.stockSymbols:
    url ='https://finnhub.io/api/v1/stock/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
    dataset = u.getDataFromApi(url)
    stockHistoricalDataList.append(dataset['c'])

  dataframe = pd.DataFrame(data=stockHistoricalDataList, index = c.stockSymbols)
  dataframeTrasposed = dataframe.transpose()
  u.insertInDB(dataframeTrasposed, 'stockHistoricalData')


def createExchangeRatesHistoricalDataTable():
  FROM = str(getDateFrom())
  TO = str(getDateTo())
  exchangeRatesHistoricalDataList = list()

  for symbol in c.exchangeSymbols:
    url = 'https://finnhub.io/api/v1/forex/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
    dataset = u.getDataFromApi(url)
    exchangeRatesHistoricalDataList.append(dataset['c'])
  
  dataframe = pd.DataFrame(data=exchangeRatesHistoricalDataList, index = c.exchanges)
  dataframeTrasposed = dataframe.transpose()
  u.insertInDB(dataframeTrasposed, 'exchangeRatesHistoricalData')


def createTables():
  createStockAnagraphicDataTable()
  createStockHistoricalDataTable()
  createExchangeRatesHistoricalDataTable()
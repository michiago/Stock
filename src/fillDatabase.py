from interactionDB import InteractionDB
from interactionAPI import InteractionAPI
import constants as c
import utils as u
import pandas as pd
import time
import datetime



def getDateFrom():
  FROM = datetime.date.today() - datetime.timedelta(365)
  return int(time.mktime(FROM.timetuple()))

def getDateTo():
  TO = datetime.date.today()
  return int(time.mktime(TO.timetuple()))


def createStockAnagraphicDataTable():
  
  stockAnagraphicDataList = list()
  count = 0

  for symbol in c.stockSymbols:
    url ='https://finnhub.io/api/v1/stock/profile2?symbol='+symbol+'&token='+c.TOKEN   
    int_api = InteractionAPI(url)
    if int_api.hasResponse:
      dataset = int_api.getData()
      if dataset:
        stockAnagraphicDataList.append(dataset.values())
        count=count+1
        if count == 100:
          break

  dataframe = pd.DataFrame(data=stockAnagraphicDataList, columns=dataset.keys())
  InteractionDB('src/database.db').insertInDB(dataframe, 'stockAnagraphicData')


def createStockHistoricalDataTable():
  
  FROM = str(getDateFrom())
  TO = str(getDateTo())
  stockHistoricalDataList = list()
  availableStockSymbols = list()
  count = 0

  for symbol in c.stockSymbols:
    url ='https://finnhub.io/api/v1/stock/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token='+c.TOKEN
    int_api = InteractionAPI(url)
    if int_api.hasResponse:
      dataset = int_api.getData()
      if(dataset and dataset['s'] == 'ok'):
        stockHistoricalDataList.append(dataset['c'])
        availableStockSymbols.append(symbol)
        count=count+1
        if count == 100:
          break


  dataframe = pd.DataFrame(data=stockHistoricalDataList, index = availableStockSymbols)
  dataframeTrasposed = dataframe.transpose()
  InteractionDB('src/database.db').insertInDB(dataframeTrasposed, 'stockHistoricalData')


def createExchangesRateAnagraphicDataTable():
  exchangesRateAnagraphicDataList = list ()
  
  for agency in c.agencies:
    url ='https://finnhub.io/api/v1/forex/symbol?exchange='+agency+'&token='+c.TOKEN 
    int_api = InteractionAPI(url)
    if(int_api.hasResponse):
      dataset = int_api.getData()
      if(dataset):
        for elem in dataset: 
          if(elem['displaySymbol'] in c.requiredExchangeRates):
            row = [agency, elem['description'], elem['displaySymbol'], elem['symbol']]
            exchangesRateAnagraphicDataList.append(row)

  dataframe = pd.DataFrame(data=exchangesRateAnagraphicDataList, columns = ['agency', 'description', 'displaySymbol', 'symbol'])
  InteractionDB('src/database.db').insertInDB(dataframe, 'exchangesRateAnagraphicData')


def createExchangeRatesHistoricalDataTable():
  FROM = str(getDateFrom())
  TO = str(getDateTo())
  exchangeRatesHistoricalDataList = list()

  for symbol in c.exchangeSymbols:
    url = 'https://finnhub.io/api/v1/forex/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token='+c.TOKEN 
    int_api = InteractionAPI(url)
    if(int_api.hasResponse):
      dataset = int_api.getData()
      if(dataset and dataset['s'] == 'ok'):
        exchangeRatesHistoricalDataList.append(dataset['c'])

  dataframe = pd.DataFrame(data=exchangeRatesHistoricalDataList, index = c.exchangesDisplaySymbols)
  dataframeTrasposed = dataframe.transpose()
  InteractionDB('src/database.db').insertInDB(dataframeTrasposed, 'exchangeRatesHistoricalData')


def createTables():
  createStockAnagraphicDataTable()
  createStockHistoricalDataTable()
  createExchangesRateAnagraphicDataTable()
  createExchangeRatesHistoricalDataTable()
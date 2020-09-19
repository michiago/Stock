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
  for symbol in c.stockSymbols:
    url ='https://finnhub.io/api/v1/stock/profile2?symbol='+symbol+'&token=btg5t0f48v6r32agadkg'
    dataset = InteractionAPI(url).getDataFromApi()
    stockAnagraphicDataList.append(dataset.values())

  dataframe = pd.DataFrame(data=stockAnagraphicDataList, columns = dataset.keys())
  InteractionDB('src/database.db').insertInDB(dataframe, 'stockAnagraphicData')


def createStockHistoricalDataTable():
  FROM = str(getDateFrom())
  TO = str(getDateTo())
  stockHistoricalDataList = list()

  for symbol in c.stockSymbols:
    url ='https://finnhub.io/api/v1/stock/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
    dataset = InteractionAPI(url).getDataFromApi()
    stockHistoricalDataList.append(dataset['c'])

  dataframe = pd.DataFrame(data=stockHistoricalDataList, index = c.stockSymbols)
  dataframeTrasposed = dataframe.transpose()
  InteractionDB('src/database.db').insertInDB(dataframeTrasposed, 'stockHistoricalData')


def createExchangesRateAnagraphicDataTable():
  exchangesRateAnagraphicDataList = list ()
  
  for agency in c.agencies:
    url =('https://finnhub.io/api/v1/forex/symbol?exchange='+agency+'&token=btg5t0f48v6r32agadkg')
    dataset = InteractionAPI(url).getDataFromApi()
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
    url = 'https://finnhub.io/api/v1/forex/candle?symbol='+symbol+'&resolution=W&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
    dataset = InteractionAPI(url).getDataFromApi()
    exchangeRatesHistoricalDataList.append(dataset['c'])
  
  dataframe = pd.DataFrame(data=exchangeRatesHistoricalDataList, index = c.exchangesDisplaySymbols)
  dataframeTrasposed = dataframe.transpose()
  InteractionDB('src/database.db').insertInDB(dataframeTrasposed, 'exchangeRatesHistoricalData')


def createTables():
  createStockAnagraphicDataTable()
  createStockHistoricalDataTable()
  createExchangesRateAnagraphicDataTable()
  createExchangeRatesHistoricalDataTable()
import constants as c

import plotext.plot as plx
import sqlite3
import pandas
import requests
import json


def isStockSymbolInvalid(stockSymbol):
    if(stockSymbol not in c.stockSymbols):
        print('ERROR: This stock symbol is not supported')
        return True

# to improve
def isCurrencyInvalid(currencySymbol):
    if(currencySymbol not in c.currencyAll):
        print('ERROR: This currency is not supported')
        return True

def drowTheGraph(subject):
    plx.clear_plot()
    plx.scatter(subject)
    plx.show()


def getQueryFromDB(query):
    connection = sqlite3.connect('src/database.db')
    exchanges = pandas.read_sql_query(query, connection)
    connection.close()

def insertInDB(dataframe, tableName):
    connection = sqlite3.connect('src/database.db')
    dataframe.to_sql(tableName, connection, if_exists='replace', index=False)
    connection.close()

def getDataFromApi(url):
    content = requests.get(url).content
    return json.loads(content)


def convertToUSD(currency):
    exchanges = getQueryFromDB( 'select ' +currency+ ' from exchangeRatesHistoricalData', connection)
    return exchanges[exchanges.columns[0]]

def convertFromUSD(currency):
    return 1/convertToUSD(currency)
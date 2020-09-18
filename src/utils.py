import constants as c
import plotext.plot as plx

import sqlite3
import pandas as pd

def isStockSymbolInvalid(stockSymbol):
    if(stockSymbol not in c.stockSymbols):
        print('ERROR: This stock symbol is not supported')
        return True

def isCurrencyInvalid(currencySymbol):
    if(currencySymbol not in c.currencyAll):
        print('ERROR: This currency is not supported')
        return True

def drowTheGraph(subject):
    plx.clear_plot()
    plx.scatter(subject)
    plx.show()

def convertToUSD(currency):
    connection = sqlite3.connect('database.db')
    exchanges = pd.read_sql_query( 'select ' +currency+ ' from exchangeRatesHistoricalData', connection)
    connection.close()
    return exchanges[exchanges.columns[0]]

def convertFromUSD(currency):
    return 1/convertToUSD(currency)
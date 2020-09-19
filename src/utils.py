import constants as c

import plotext.plot as plx
import sqlite3
import pandas
import requests
import json
import time
import datetime


def isStockSymbolInvalid(stockSymbol):
    if(stockSymbol not in c.stockSymbols):
        print('ERROR: This stock symbol is not supported')
        return True
    return False


def isCurrencyConvertionInvalid(currencySymbol):
    if(currencySymbol not in c.currencyAll):
        print('ERROR: This currency is not supported')
        return True
    return False


def isCurrencyHistoricalInvalid(currencySymbol):
    if(currencySymbol not in c.currencyHistorical):
        print('ERROR: This currency is not supported')
        return True
    return False


def isDateFormatInvalid(dateString):
    try:
        datetime.datetime.strptime(dateString, '%Y-%m-%d')
    except ValueError:
        print('ERROR: Incorrect data format')
        return True
    else:
        return False


def areDatesInconsistent(day1, day2):
    date1 = datetime.datetime.strptime(day1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(day2, '%Y-%m-%d')

    dateOrdered = date1 < date2
    dateInThePast = date2 <= datetime.datetime.now()

    if(dateOrdered and dateInThePast):
        return False
    else:
        print('Dates are inconsistent')
        return True


def getUnixFormatFromString(dateString):
    dateParts = dateString.split('-')
    date = datetime.datetime(int(dateParts[0]), int(dateParts[1]), int(dateParts[2]))
    return str(int(time.mktime(date.timetuple())))


def drowTheGraph(subject):
    plx.clear_plot()
    plx.scatter(subject)
    plx.show()


def getQueryFromDB(query):
    connection = sqlite3.connect('src/database.db')
    data = pandas.read_sql_query(query, connection)
    connection.close()
    return data


def insertInDB(dataframe, tableName):
    connection = sqlite3.connect('src/database.db')
    dataframe.to_sql(tableName, connection, if_exists='replace', index=False)
    connection.close()


def getDataFromApi(url):
    content = requests.get(url).content
    return json.loads(content)


def convertToUSD(currency):
    exchanges = getQueryFromDB( 'select ' +currency+ ' from exchangeRatesHistoricalData')
    return exchanges[exchanges.columns[0]]


def convertFromUSD(currency):
    return 1/convertToUSD(currency)
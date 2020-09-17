import constants as c

import requests
import json
import sqlite3
import pandas as pd
import plotext.plot as plx


def getHistoricalQuotes():

    MENU_PROMPT = """Enter a stock symbol: """
    stockSymbol = input(MENU_PROMPT)
    if(stockSymbol not in c.stockSymbols):
        print('ERROR: This stock symbol is not supported')
        return
    
    MENU_PROMPT = """Enter a currency symbol:
    - 'USD'
    - 'EUR'
    - 'AUD'
    - 'GBP'
    - 'ALL' to get the conversion in all the above currency
    Your choice: """
    currencySymbol = input(MENU_PROMPT)
    if(currencySymbol not in c.currencyAll):
        print('ERROR: This option is not available')
        return
    
    connection = sqlite3.connect('database.db')
    USDquotes = pd.read_sql_query( 'select ' + stockSymbol + ' from stockHistoricalData', connection)
    usd=USDquotes[stockSymbol]
    
    if(currencySymbol == 'USD' or currencySymbol == 'ALL'):         
        print("""The USD historical quotes of the stock {} are: 
        {}""".format(stockSymbol, usd))
    
    if(currencySymbol == 'EUR' or currencySymbol == 'ALL'):  
        EURexchange = pd.read_sql_query( 'select EUR from exchangeRatesHistoricalData', connection)
        eur=(EURexchange['EUR'])
        print("""The EUR historical quotes of the stock {} are: 
        {}""".format(stockSymbol, usd * 1/eur))

    if(currencySymbol == 'AUD' or currencySymbol == 'ALL'):  
        AUDexchange = pd.read_sql_query( 'select AUD from exchangeRatesHistoricalData', connection)
        aud=(AUDexchange['AUD'])
        print("""The AUD historical quotes of the stock {} are: 
        {}""".format(stockSymbol, usd * 1/aud))

    if(currencySymbol == 'GBP' or currencySymbol == 'ALL'):  
        GBPexchange = pd.read_sql_query( 'select GBP from exchangeRatesHistoricalData', connection)
        gbp=(GBPexchange['GBP'])
        print("""The GBP historical quotes of the stock {} are: 
        {}""".format(stockSymbol, usd * 1/gbp))

    connection.close()



def getLatestQuote():

    MENU_PROMPT = """Enter a stock symbol: """
    stockSymbol = input(MENU_PROMPT)
    if(stockSymbol not in c.stockSymbols):
        print('ERROR: This stock symbol is not supported')
        return

    MENU_PROMPT = """Enter a currency symbol:
    - 'USD' to get the base value
    - 'EUR' to get the base value converted in eur
    - 'AUD' to get the base value converted in aud
    - 'GBP' to get the base value converted in gbp
    Your choice: """
    currencySymbol = input(MENU_PROMPT)
    if(currencySymbol not in c.currency):
        print('ERROR: This currency is not available')
        return

    url = 'https://finnhub.io/api/v1/quote?symbol='+stockSymbol+'&token=btg5t0f48v6r32agadkg'
    content = requests.get(url).content
    dataset = json.loads(content)
    currentQuote = dataset['c']

    if(currencySymbol != 'USD'):
        connection = sqlite3.connect('database.db')
        convertions = pd.read_sql_query( 'select ' +currencySymbol+ ' from exchangeRatesHistoricalData', connection)
        convertion=(convertions[currencySymbol].iloc[-1])
        currentQuote = currentQuote * 1/convertion
        connection.close()

    print("The {} latest quote of the stock {} is: {} ".format(currencySymbol, stockSymbol, currentQuote))



def convertToUSD(currency):
    connection = sqlite3.connect('database.db')
    exchanges = pd.read_sql_query( 'select ' +currency+ ' from exchangeRatesHistoricalData', connection)
    connection.close()
    return exchanges[exchanges.columns[0]]

def convertFromUSD(currency):
    return 1/convertToUSD(currency)

def getGraphHistoricalExchangeRate():

    MENU_PROMPT = """Enter the currency symbol FROM:
    - 'USD' 
    - 'EUR' 
    - 'AUD' 
    - 'GBP'
    Your choice: """
    currencyFrom = input(MENU_PROMPT)
    if(currencyFrom not in c.currency):
        print('ERROR: This currency is not available')
        return
    
    MENU_PROMPT = """Enter the currency symbol TO:
    - 'USD' 
    - 'EUR' 
    - 'AUD' 
    - 'GBP'
    Your choice: """
    currencyTo = input(MENU_PROMPT)
    if(currencyTo == currencyFrom):
        print("ERROR: FROM and TO can't be equal")
        return
    if(currencyTo not in c.currency):
        print('ERROR: This currency is not available')
        return

    if(currencyTo == 'USD'):
        exchanges = convertToUSD(currencyFrom)
    elif(currencyFrom == 'USD'):
        exchanges = convertFromUSD(currencyTo)    
    else:
        exchanges = convertToUSD(currencyFrom) * convertFromUSD(currencyTo)

    plx.clear_plot()
    plx.scatter(exchanges.values.tolist())
    plx.show()



def getGraphHistoricalQuotes():
    
    MENU_PROMPT = """Enter a stock symbol: """
    stockSymbol = input(MENU_PROMPT)
    if(stockSymbol not in c.stockSymbols):
        print('ERROR: This stock symbol is not supported')
        return

    connection = sqlite3.connect('database.db')
    quotes = pd.read_sql_query( 'select ' +stockSymbol+ ' from stockHistoricalData', connection)
    connection.close()
    
    toPrint = quotes[quotes.columns[0]].values.tolist()
    plx.clear_plot()
    plx.scatter(toPrint)
    plx.show()



def isIntervalConsistent(timeBegin, timeEnd):
    return True


def getGraphHistoricalIntervalQuotes():

    MENU_PROMPT = """Enter a stock symbol: """
    stockSymbol = input(MENU_PROMPT)
    if(stockSymbol not in c.stockSymbols):
        print('ERROR: This stock symbol is not supported')
        return
    
    MENU_PROMPT = """Enter the begin of your desired time interval in format Unix Timestamp: """
    FROM = input(MENU_PROMPT)
    FROM = '1596240000'
    
    MENU_PROMPT = """Enter the end of your desired time interval in format Unix Timestamp: """
    TO = input(MENU_PROMPT)
    TO = '1598832000'

    if (not isIntervalConsistent(FROM, TO)):
        return

    url ='https://finnhub.io/api/v1/stock/candle?symbol='+stockSymbol+'&resolution=D&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
    content = requests.get(url).content
    dataset = json.loads(content)

    plx.clear_plot()
    plx.scatter(dataset['c'])
    plx.show()

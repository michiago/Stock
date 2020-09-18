import constants as c
import utils as u

import requests
import json
import sqlite3
import pandas as pd



def getHistoricalQuotes():
  
    stockSymbol = input(c.askOneStock)        
    if(u.isStockSymbolInvalid(stockSymbol)):
        return
    currencySymbol = input(c.askOneCurrencyOrAll)
    if(u.isCurrencyInvalid(currencySymbol)): 
        return
    
       
    connection = sqlite3.connect('database.db')
    USDquotes = pd.read_sql_query( 'select ' + stockSymbol + ' from stockHistoricalData', connection)
    usd=USDquotes[stockSymbol]
    
    if(currencySymbol == 'USD' or currencySymbol == 'ALL'):         
        print(f"The USD historical quotes of the stock {stockSymbol} are: {usd}")
    
    if(currencySymbol == 'EUR' or currencySymbol == 'ALL'):  
        EURexchange = pd.read_sql_query( 'select EUR from exchangeRatesHistoricalData', connection)
        eur=(EURexchange['EUR'])
        print(f"The EUR historical quotes of the stock {stockSymbol} are: {usd * 1/eur}")

    if(currencySymbol == 'AUD' or currencySymbol == 'ALL'):  
        AUDexchange = pd.read_sql_query( 'select AUD from exchangeRatesHistoricalData', connection)
        aud=(AUDexchange['AUD'])
        print(f"The AUD historical quotes of the stock {stockSymbol} are: {usd * 1/aud}")

    if(currencySymbol == 'GBP' or currencySymbol == 'ALL'):  
        GBPexchange = pd.read_sql_query( 'select GBP from exchangeRatesHistoricalData', connection)
        gbp=(GBPexchange['GBP'])
        print(f"The GBP historical quotes of the stock {stockSymbol} are: {usd * 1/gbp}")

    connection.close()



def getLatestQuote():

    # Get inputs
    stockSymbol = input(c.askOneStock)        
    if(u.isStockSymbolInvalid(stockSymbol)):
        return
    currencySymbol = input(c.askOneCurrencyOrAll)
    if(u.isCurrencyInvalid(currencySymbol)): 
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

    print(f"The {currencySymbol} latest quote of the stock {stockSymbol} is: {currentQuote} ")



def getGraphHistoricalExchangeRate():

    # Get inputs
    currencyFrom = input(c.askCurrencyFrom)   
    if(u.isCurrencyInvalid(currencyFrom) ):
        return
    
    currencyTo = input(c.askCurrencyTo)
    if(u.isCurrencyInvalid(currencyTo)):
        return
    if(currencyTo == currencyFrom):
        print("ERROR: FROM and TO can't be equal")
        return

    # Compute
    if(currencyTo == 'USD'):
        exchanges = u.convertToUSD(currencyFrom)
    elif(currencyFrom == 'USD'):
        exchanges = u.convertFromUSD(currencyTo)    
    else:
        exchanges = u.convertToUSD(currencyFrom) * u.convertFromUSD(currencyTo)

    # Print
    u.drowTheGraph(exchanges.values.tolist())



def getGraphHistoricalQuotes():

    # Get inputs  
    stockSymbol = input(c.askOneStock)
    if(u.isStockSymbolInvalid(stockSymbol)):
        return

    # Compute
    connection = sqlite3.connect('database.db')
    quotes = pd.read_sql_query( 'select ' +stockSymbol+ ' from stockHistoricalData', connection)
    connection.close()
    
    # Print
    u.drowTheGraph(quotes[quotes.columns[0]].values.tolist())



def getGraphHistoricalIntervalQuotes():

    # Get inputs
    stockSymbol = input(c.askOneStock)
    if(u.isStockSymbolInvalid(stockSymbol)):
        return
        
    FROM = input(c.askBeginInterval)
    FROM = '1596240000'
    
    TO = input(c.askEndInterval)
    TO = '1598832000'


    # Retrive data
    url ='https://finnhub.io/api/v1/stock/candle?symbol='+stockSymbol+'&resolution=D&from='+FROM+'&to='+TO+'&token=btg5t0f48v6r32agadkg'
    content = requests.get(url).content
    dataset = json.loads(content)

    # Print
    u.drowTheGraph(dataset['c'])

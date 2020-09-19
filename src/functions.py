import constants as c
import utils as u

import requests
import json
import sqlite3
import pandas as pd



def getHistoricalQuotes():
  
    # Input
    stockSymbol = input(c.askOneStock)        
    if(u.isStockSymbolInvalid(stockSymbol)):
        return
    currencySymbol = input(c.askOneCurrency)
    if(u.isCurrencyInvalid(currencySymbol)): 
        return

    # Retrieve information
    USDquotes = u.getQueryFromDB( 'select ' + stockSymbol + ' from stockHistoricalData', connection)
    usd=USDquotes[stockSymbol]

    url = 'https://finnhub.io/api/v1/forex/rates?base=USD&token=btg5t0f48v6r32agadkg'
    dataset = u.getDataFromApi(url)
    convertion = dataset['quote'][currencySymbol]
    print(convertion)

   # Return        
    print(f"The {currencySymbol} historical quotes of the stock {stockSymbol} are: {usd*convertion}") 



def getLatestQuote():

    # Get inputs
    stockSymbol = input(c.askOneStock)        
    if(u.isStockSymbolInvalid(stockSymbol)):
        return
    currencySymbol = input(c.askOneCurrency)
    if(u.isCurrencyInvalid(currencySymbol)): 
        return

    # Retrieve information
    url = 'https://finnhub.io/api/v1/quote?symbol='+stockSymbol+'&token=btg5t0f48v6r32agadkg'
    dataset = u.getDataFromApi(url)
    currentQuote = dataset['c']

    convertion = 1
    if(currencySymbol != 'USD'):
        url = 'https://finnhub.io/api/v1/forex/rates?base=USD&token=btg5t0f48v6r32agadkg'
        dataset = u.getDataFromApi(url)
        convertion = dataset['quote'][currencySymbol]

    # Return
    print(f"The {currencySymbol} latest quote of the stock {stockSymbol} is: {currentQuote * convertion} ")



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
    quotes = u.getQueryFromDB( 'select ' +stockSymbol+ ' from stockHistoricalData', connection)
    
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
    dataset = u.getDataFromApi(url)

    # Print
    u.drowTheGraph(dataset['c'])

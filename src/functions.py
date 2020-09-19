import constants as c
import utils as u

import requests
import json
import sqlite3
import pandas as pd



def getHistoricalQuotes():
  
    # Input
    stockSymbol = (input(c.askOneStock)).upper()
    if(u.isStockSymbolInvalid(stockSymbol)):
        return
    currencySymbol = (input(c.askOneCurrency)).upper()
    if(u.isCurrencyConvertionInvalid(currencySymbol)): 
        return

    # Retrieve information
    USDquotes = u.getQueryFromDB( 'select ' + stockSymbol + ' from stockHistoricalData')
    usd=USDquotes[stockSymbol]

    url = 'https://finnhub.io/api/v1/forex/rates?base=USD&token=btg5t0f48v6r32agadkg'
    dataset = u.getDataFromApi(url)
    convertion = dataset['quote'][currencySymbol]

    requiredQuotes = (usd*convertion).values.tolist()


   # Return        
    print(f"The {currencySymbol} historical quotes of the stock {stockSymbol} are: {requiredQuotes}") 


def getLatestQuote():

    # Get inputs
    stockSymbol = (input(c.askOneStock)).upper()      
    if(u.isStockSymbolInvalid(stockSymbol)):
        return
    currencySymbol = (input(c.askOneCurrency)).upper()
    if(u.isCurrencyConvertionInvalid(currencySymbol)): 
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
    currencyFrom = (input(c.askCurrencyFrom)).upper()
    if(u.isCurrencyHistoricalInvalid(currencyFrom) ):
        return
    
    currencyTo = (input(c.askCurrencyTo)).upper()
    if(u.isCurrencyHistoricalInvalid(currencyTo)):
        return
    if(currencyTo == currencyFrom):
        print("ERROR: FROM and TO can't be equal")
        return

    # Retrieve the information
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
    stockSymbol = (input(c.askOneStock)).upper()
    if(u.isStockSymbolInvalid(stockSymbol)):
        return

    # Retrieve the information
    quotes = u.getQueryFromDB( 'select ' +stockSymbol+ ' from stockHistoricalData')
    
    # Print
    u.drowTheGraph(quotes[quotes.columns[0]].values.tolist())


def getGraphHistoricalIntervalQuotes():

    # Get inputs
    stockSymbol = (input(c.askOneStock)).upper()
    if(u.isStockSymbolInvalid(stockSymbol)):
        return
        
    FROM = input(c.askBeginInterval)
    if(u.isDateFormatInvalid(FROM)):
        return
    TO = input(c.askEndInterval)
    if(u.isDateFormatInvalid(TO)):
        return   
    if(u.areDatesInconsistent(FROM, TO)):
        return

    FROMunix = u.getUnixFormatFromString(FROM)
    TOunix = u.getUnixFormatFromString(TO)


    # Retrieve the information
    url ='https://finnhub.io/api/v1/stock/candle?symbol='+stockSymbol+'&resolution=D&from='+FROMunix+'&to='+TOunix+'&token=btg5t0f48v6r32agadkg'
    dataset = u.getDataFromApi(url)

    # Print
    u.drowTheGraph(dataset['c'])

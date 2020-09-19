import constants as c
import utils as u
from interactionDB import InteractionDB
from inputValidator import InputValidator
from interactionAPI import InteractionAPI



def getHistoricalQuotes():
  
    # Input
    stockSymbol = (input(c.askOneStock)).upper()
    if(InputValidator().isStockSymbolInvalid(stockSymbol)):
        return
    currencySymbol = (input(c.askOneCurrency)).upper()
    if(InputValidator().isCurrencyConvertionInvalid(currencySymbol)): 
        return

    # Retrieve information
    USDquotes = InteractionDB('src/database.db').getQueryFromDB( 'select ' + stockSymbol + ' from stockHistoricalData')
    usd=USDquotes[stockSymbol]

    url = 'https://finnhub.io/api/v1/forex/rates?base=USD&TOKEN='+c.TOKEN
    int_api = InteractionAPI(url)
    if(not int_api.hasResponse):
        print('Sorry, an error while retrieving data with the API occurred')
        return   
    dataset = int_api.getData()
    convertion = dataset['quote'][currencySymbol]

    requiredQuotes = (usd*convertion).values.tolist()


   # Return        
    print(f"The {currencySymbol} historical quotes of the stock {stockSymbol} are: {requiredQuotes}") 


def getLatestQuote():

    # Get inputs
    stockSymbol = (input(c.askOneStock)).upper()      
    if(InputValidator().isStockSymbolInvalid(stockSymbol)):
        return
    currencySymbol = (input(c.askOneCurrency)).upper()
    if(InputValidator().isCurrencyConvertionInvalid(currencySymbol)): 
        return

    # Retrieve information
    url = 'https://finnhub.io/api/v1/quote?symbol='+stockSymbol+'&token='+c.TOKEN
    int_api = InteractionAPI(url)
    if(not int_api.hasResponse):
        print('Sorry, an error while retrieving data with the API occurred')
        return   
    dataset = int_api.getData()
    currentQuote = dataset['c']

    convertion = 1
    if(currencySymbol != 'USD'):
        url = 'https://finnhub.io/api/v1/forex/rates?base=USD&token='+c.TOKEN
        int_api = InteractionAPI(url)
        if(not int_api.hasResponse):
            print('Sorry, an error while retrieving data with the API occurred')
            return   
        dataset = int_api.getData()
        convertion = dataset['quote'][currencySymbol]

    # Return
    print(f"The {currencySymbol} latest quote of the stock {stockSymbol} is: {currentQuote * convertion} ")


def getGraphHistoricalExchangeRate():

    # Get inputs
    currencyFrom = (input(c.askCurrencyFrom)).upper()
    if(InputValidator().isCurrencyHistoricalInvalid(currencyFrom) ):
        return
    
    currencyTo = (input(c.askCurrencyTo)).upper()
    if(InputValidator().isCurrencyHistoricalInvalid(currencyTo)):
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
    if(InputValidator().isStockSymbolInvalid(stockSymbol)):
        return

    # Retrieve the information
    quotes = InteractionDB('src/database.db').getQueryFromDB( 'select ' +stockSymbol+ ' from stockHistoricalData')
    
    # Print
    u.drowTheGraph(quotes[quotes.columns[0]].values.tolist())


def getGraphHistoricalIntervalQuotes():

    # Get inputs
    stockSymbol = (input(c.askOneStock)).upper()
    if(InputValidator().isStockSymbolInvalid(stockSymbol)):
        return
        
    FROM = input(c.askBeginInterval)
    if(InputValidator().isDateFormatInvalid(FROM)):
        return
    TO = input(c.askEndInterval)
    if(InputValidator().isDateFormatInvalid(TO)):
        return   
    if(InputValidator().areDatesInconsistent(FROM, TO)):
        return

    FROMunix = u.getUnixFormatFromString(FROM)
    TOunix = u.getUnixFormatFromString(TO)


    # Retrieve the information
    url ='https://finnhub.io/api/v1/stock/candle?symbol='+stockSymbol+'&resolution=D&from='+FROMunix+'&to='+TOunix+'&token='+c.TOKEN
    int_api = InteractionAPI(url)
    if(not int_api.hasResponse):
        print('Sorry, an error while retrieving data with the API occurred')
        return   
    dataset = int_api.getData()


    # Print
    u.drowTheGraph(dataset['c'])

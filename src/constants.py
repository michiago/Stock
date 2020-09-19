from interactionAPI import InteractionAPI

# Stock symbols supported
url = ('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=btg5t0f48v6r32agadkg')
dataset = InteractionAPI(url).getDataFromApi()
stockSymbols = list()
for elem in dataset:
    stockSymbols.append(elem['symbol'])
stockSymbols = stockSymbols[0:20]


# Currency supported for conversion
url = ('https://finnhub.io/api/v1/forex/rates?base=USD&token=btg5t0f48v6r32agadkg')
dataset = InteractionAPI(url).getDataFromApi()
currencyAll = dataset['quote'].keys()

# Agencies providing forex exchanges
url = ('https://finnhub.io/api/v1/forex/exchange?token=btg5t0f48v6r32agadkg')
dataset = InteractionAPI(url).getDataFromApi()
agencies = dataset

# Currencies supported for historical data
currencyHistorical = ['USD', 'EUR', 'AUD', 'GBP']

# Exchanges display supported
requiredExchangeRates = ['EUR/USD', 'AUD/USD', 'GBP/USD']

# Exchange symbols supported for agency oanda
url =('https://finnhub.io/api/v1/forex/symbol?exchange=oanda&token=btg5t0f48v6r32agadkg')
dataset = InteractionAPI(url).getDataFromApi()
exchangeSymbols = list()
exchangesDisplaySymbols = list()
for elem in dataset:
    if(elem['displaySymbol'] in requiredExchangeRates):
        exchangeSymbols.append(elem['symbol'])
        exchangesDisplaySymbols.append(elem['displaySymbol'][0:3])




menuApp = """Enter:
- '1' to get historical stock quotes in any foreign currency
- '2' to get the latest quote for a given asset
- '3' to get a graph of the whole historical data for an exchange rate
- '4' to get a graph of the whole historical data for a stock
- '5' to get a graph of the historical data for a stock in a given interval of time
- 'q' to quit
Your choice: """

askOneStock = "Enter a stock symbol: "

askOneCurrency = "Enter a currency symbol: "

askCurrencyFrom = "Enter the currency symbol FROM among the availables ("
for currency in currencyHistorical:
    askCurrencyFrom = askCurrencyFrom + " " + currency + " "
askCurrencyFrom = askCurrencyFrom + ") Your choice: "


askCurrencyTo = "Enter the currency symbol FROM among the availables ("
for currency in currencyHistorical:
    askCurrencyTo = askCurrencyTo + " " + currency + " "
askCurrencyTo = askCurrencyTo + ") Your choice: "

askBeginInterval = "Enter the begin of your desired time interval in format yyyy-mm-dd: "

askEndInterval = "Enter the end of your desired time interval in format yyyy-mm-dd: "
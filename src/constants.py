stockSymbols = ['AAPL', 'ABT']
exchangeSymbols = ['OANDA:EUR_USD', 'OANDA:AUD_USD', 'OANDA:GBP_USD']
exchanges = ['EUR', 'AUD', 'GBP']
currencyAll = ['USD', 'EUR', 'AUD', 'GBP', 'ALL']
currency = ['USD', 'EUR', 'AUD', 'GBP']

menuApp = """Enter:
- '1' to get historical stock quotes in any foreign currency
- '2' to get the latest quote for a given asset
- '3' to get a graph of the whole historical data for an exchange rate
- '4' to get a graph of the whole historical data for a stock
- '5' to get a graph of the historical data for a stock in a given interval of time
- 'q' to quit
Your choice: """

askOneStock = """Enter a stock symbol: """

askOneCurrencyOrAll = """Enter a currency symbol:
- 'USD'
- 'EUR'
- 'AUD'
- 'GBP'
- 'ALL' to get the conversion in all the above currency
Your choice: """

askOneCurrency = """Enter a currency symbol:
- 'USD' to get the base value
- 'EUR' to get the base value converted in eur
- 'AUD' to get the base value converted in aud
- 'GBP' to get the base value converted in gbp
Your choice: """

askCurrencyFrom = """Enter the currency symbol FROM:
- 'USD' 
- 'EUR' 
- 'AUD' 
- 'GBP'
Your choice: """

askCurrencyTo = """Enter the currency symbol TO:
- 'USD' 
- 'EUR' 
- 'AUD' 
- 'GBP'
Your choice: """

askBeginInterval = """Enter the begin of your desired time interval in format Unix Timestamp: """

askEndInterval = """Enter the end of your desired time interval in format Unix Timestamp: """
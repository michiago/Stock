from src.interactionAPI import InteractionAPI

TOKEN = "btj358748v6p9f1pnq2g"

# Stock symbols supported
url = "https://finnhub.io/api/v1/stock/symbol?exchange=US&token=" + TOKEN
dataset = InteractionAPI(url).getData()
stockSymbols = list()
for elem in dataset:
    stockSymbols.append(elem["symbol"])


# Currency supported for conversion
url = "https://finnhub.io/api/v1/forex/rates?base=USD&token=" + TOKEN
dataset = InteractionAPI(url).getData()
currencyAll = dataset["quote"].keys()

# Agencies providing forex exchanges
url = "https://finnhub.io/api/v1/forex/exchange?token=" + TOKEN
dataset = InteractionAPI(url).getData()
agencies = dataset

# Currencies supported for historical data
currencyHistorical = ["USD", "EUR", "AUD", "GBP"]

# Exchanges display supported
requiredExchangeRates = ["EUR/USD", "AUD/USD", "GBP/USD"]

# Exchange symbols supported for agency oanda
url = "https://finnhub.io/api/v1/forex/symbol?exchange=oanda&token=" + TOKEN
dataset = InteractionAPI(url).getData()
exchangeSymbols = list()
exchangesDisplaySymbols = list()
for elem in dataset:
    if elem["displaySymbol"] in requiredExchangeRates:
        exchangeSymbols.append(elem["symbol"])
        exchangesDisplaySymbols.append(elem["displaySymbol"][0:3])


menuApp = """Enter:
- '1': to get historical stock quotes for a given stock and a given currency
- '2': to get the latest quote for a given stock
- '3': to get a graph of the whole historical exchange rates for a given from/to currency
- '4': to get a graph of the whole historical stock quotes for a given stock
- '5': to get a graph of the historical stock quotes for a given stock and a given time interval
- 'q': to quit
Your choice: """

askOneStock = "Enter a stock symbol (e.g. AAPL): "

askOneCurrency = "Enter a currency symbol (e.g. USD): "


askCurrencyText = (
    "Enter the currency symbol <DIRECTION>, among the availables: \n"
    + "\n".join(["- " + x for x in currencyHistorical])
    + "\nYour choice: "
)

askCurrencyFrom = askCurrencyText.replace("<DIRECTION>", "FROM")
askCurrencyTo = askCurrencyText.replace("<DIRECTION>", "TO")


askBeginInterval = "Enter the begin of your desired time interval in format yyyy-mm-dd: "

askEndInterval = "Enter the end of your desired time interval in format yyyy-mm-dd: "
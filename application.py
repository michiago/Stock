import functions as f

MENU_PROMPT = """Enter:
- '1' to get historical stock quotes in any foreign currency
- '2' to get the latest quote for a given asset
- '3' to get a graph of the whole historical data for an exchange rate
- '4' to get a graph of the whole historical data for a stock
- '5' to get a graph of the historical data for a stock in a given interval of time
- 'q' to quit
Your choice: """

def menu():
    """ The menu of the app. """
    selection = input(MENU_PROMPT)
    while selection != "q":
        if selection == "1":
            f.getHistoricalQuotes()
        elif selection == "2":
            f.getLatestQuote()
        elif selection == "3":
            f.getGraphHistoricalExchangeRate()
        elif selection == "4":
            f.getGraphHistoricalQuotes()
        elif selection == "5":
            f.getGraphHistoricalIntervalQuotes()
        selection = input(MENU_PROMPT)
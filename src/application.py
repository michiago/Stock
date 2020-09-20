import src.functions as f
import src.constants as c


def menu():
    selection = input(c.menuApp)
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
        selection = input(c.menuApp)
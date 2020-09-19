import time
import datetime
import constants as c

class InputValidator:


    def isStockSymbolInvalid(self, stockSymbol):
        if(stockSymbol not in c.stockSymbols):
            print('ERROR: This stock symbol is not supported')
            return True
        return False


    def isCurrencyConvertionInvalid(self, currencySymbol):
        if(currencySymbol not in c.currencyAll):
            print('ERROR: This currency is not supported')
            return True
        return False


    def isCurrencyHistoricalInvalid(self, currencySymbol):
        if(currencySymbol not in c.currencyHistorical):
            print('ERROR: This currency is not supported')
            return True
        return False


    def isDateFormatInvalid(self, dateString):
        try:
            datetime.datetime.strptime(dateString, '%Y-%m-%d')
        except ValueError:
            print('ERROR: Incorrect data format')
            return True
        else:
            return False


    def areDatesInconsistent(self, day1, day2):
        date1 = datetime.datetime.strptime(day1, '%Y-%m-%d')
        date2 = datetime.datetime.strptime(day2, '%Y-%m-%d')

        dateOrdered = date1 < date2
        dateInThePast = date2 <= datetime.datetime.now()

        if(dateOrdered and dateInThePast):
            return False
        else:
            print('Dates are inconsistent')
            return True
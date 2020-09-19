from interactionDB import InteractionDB
import plotext.plot as plx
import constants as c
import time
import datetime



def getUnixFormatFromString(dateString):
    date = datetime.datetime.strptime(dateString, '%Y-%m-%d')
    return str(int(time.mktime(date.timetuple())))


def drowTheGraph(subject):
    plx.clear_plot()
    plx.scatter(subject)
    plx.show()


def convertToUSD(currency):
    exchanges = InteractionDB('src/database.db').getQueryFromDB( 'select ' +currency+ ' from exchangeRatesHistoricalData')
    return exchanges[exchanges.columns[0]]


def convertFromUSD(currency):
    return 1/convertToUSD(currency)
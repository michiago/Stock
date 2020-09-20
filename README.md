# Stock

Solution implemented using the python3.8 programming language in a docker container.

I retrieve data from the [finnhub](https://finnhub.io/docs/api#forex-symbols) website.

I store historical data in a [SQLite](https://docs.python.org/3/library/sqlite3.html) database, I have chosen this solution because SQLite is a lightweight database that doesn’t require a separate server process but store the entire data as a file.

I installed the following libraries:
* [plotext](https://pypi.org/project/plotext/) as suggested, to plot data directly on the terminal,
* [requests](https://pypi.org/project/requests/) to send HTTP request, in order to ease the interaction with the API of the [finnhub](https://finnhub.io/docs/api#forex-symbols) website,
* [pandas](https://pypi.org/project/pandas/) to handle the interaction with the database, to ease the insertion of data in it and the query requests.

## How to run the code
In order to execute the application inside the docker container:
### 1) Enter the container
I created a simple script to build and run the docker image. This way you can easily access the container and run the code inside it, without polluting your local environment.
```
sh docker/run.sh
```
### 2) Execute the code
You can run the application with the following command:
```
python -m src
```
Once started the application will first ask you if you want to regenerate the database, in case of positive answer it will do it.
After that it will launch an interactive menu that will allow you to choose one functionality at a time among the 5 supported, until you decide to quit the application.
Once chosen a functionality the application will ask you to insert your inputs.

The supported functionalities are:
- 1: to get historical stock quotes for a given stock and a given currency
- 2: to get the latest quote for a given stock
- 3: to get a graph of the whole historical exchange rates for a given from/to currency
- 4: to get a graph of the whole historical stock quotes for a given stock
- 5: to get a graph of the historical stock quotes for a given stock and a given time interval
- q: to quit

### 3) Execute the tests
 ```
 python -m pytest
 ```
 I tested that the function menu(), that is prompting the interactive menu allowing the user to choose a functionality, is calling the right function according to the input received from the user.

## Choices

### Creation of database

#### stockAnagraphicData
I retrieve the list of supported stock symbols with the [Stock Symbol](https://finnhub.io/docs/api#stock-symbols) api, I use one of these stock symbols at a time to call the [Company Profile 2](https://finnhub.io/docs/api#company-profile2) api until I get 100 responses (it can happen that the API return an empty response, in this case I skip and I go to the next stock symbol). I store these 100 responses in the table.

#### stockHistoricalData
I retrieve the list of supported stock symbols with the [Stock Symbol](https://finnhub.io/docs/api#stock-symbols) api, I use one of these stock symbols at a time to call the [Stock Candle](https://finnhub.io/docs/api#stock-candles) api until I get 100 responses (it can happen that the API return an empty response, in this case I skip and I go to the next stock symbol). 
I call the api giving the time interval (from,to)=(today, today-365) with weekly resolution. I have chosen this time interval since the free api only allow to get data of the last year.
I store the close prices of these 100 responses in the table.

#### exchangeRateAnagraphicData
I retrieve the list of supported agencies that provide forex exchanges with the [Forex Exchanges](https://finnhub.io/docs/api#forex-exchanges) api. For every agency I call the [Forex Symbol](https://finnhub.io/docs/api#forex-symbols) api that return a list of supported forex exchanges. I store as a row in the database the elements of this list that satisfy the required condition of being a conversion from/to among (AUD/USD, EUR/USD, GBP/USD).

#### exchangeRatesHistoricalData
I decided to store data provided from the agency "Oanda" so for every symbol that is stored in the table "exchangeRateAnagraphicData" related to the Oanda agency I call the [Forex Candle](https://finnhub.io/docs/api#forex-candles) api with time interval (from,to)=(today, today-365) and with weekly resolution. I store the close prices of these responses in the table.

### Implementation of the functions

#### 1 getHistoricalQuotes
I retrieve the historical data of the required stock from the table "stockHistoricalData". I retrieve the currency convertion value with the api [Forex Rate](https://finnhub.io/docs/api#forex-rates). I print the result.

#### 2 getLatestQuote
I retrieve the current quote for the required stock with the [Quote](https://finnhub.io/docs/api#quote) api. I retrieve the currency convertion value with the api [Forex Rate](https://finnhub.io/docs/api#forex-rates). I print the result.

#### 3 getGraphHistoricalExchangeRate
I retrieve the historical data of the required forex exchange from the "exchangeRatesHistoricalData" table. 
If the currency to which the conversion is required is not the default USD I compute the conversion, always using data from the "exchangeRatesHistoricalData" table.
I print the graph.

#### 4 getGraphHistoricalQuotes
I retrieve the historical data of the required stock from the "stockHistoricalData" table and I print the graph.

#### 5 getGraphHistoricalQuotes
I retrieve the requested data with the api [Forex Candle](https://finnhub.io/docs/api#forex-candles) with daily resolution and I print the graph.

### Other choises
I introduced the class inputValidator to isolate all the methods needed to perform the validation of the data given as input.

I introduced the classes interactionAPI and interactionDB to hava a single element interfacing with the API/DB, handling the connections and handling the related errors.

I stored the constant value that the app needs to know all along the execution in the file constants.py. I stored some utility functions in the file utility.py
# DNDStockExchange
Some python to create and run a fantasy stock exchange.

This is a work in progress which when finished will allow you to from cli update a stock exchange and print out results from X day/s of trading.

Basic syntax is as follows:

cd into the DNDStockExchange directory

The inital database has been populated, but each company starts with 100GP value, in order to initialize your stock market I suggest running daytrade 30-100 times just to get a decent spread of value.


To simulate a day or X days of trade run daytrade:
The following example will loop for 10 days worth of trading;


python daytrade 10

to see the results you can run ticker.py to see just a single company listing you can run tickersingle.py;

python ticker.py

The following example will just output the first company listing in the database;

python tickersingle.py 1 

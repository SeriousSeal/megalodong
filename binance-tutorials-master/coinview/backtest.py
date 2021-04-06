import backtrader as bt
import btalib
from talib import abstract
import pandas as pd
# import datetime

class RSIStrategy(bt.Strategy):

    def __init__(self):
        # self.sma = btalib.sma(data.Close)
        self.rsi = bt.talib.RSI(data)


    def next(self):
        if self.rsi < 30 and not self.position:
            self.buy(size=0.01)
        
        if self.rsi > 70 and self.position:
            self.close()



cerebro = bt.Cerebro()

# fromdate = datetime.datetime.strptime('2020-07-01', '%Y-%m-%d')
# todate = datetime.datetime.strptime('2020-07-12', '%Y-%m-%d')

data = bt.feeds.GenericCSVData(dataname='2021_Jan_5m.csv', dtformat=2, compression=5, timeframe=bt.TimeFrame.Minutes)

# data = pd.read_csv("2021_Jan_5m.csv", 
#                     parse_dates=True,
#                     sep=",",
#                     names=[
#                         "Opentime",
#                         "Open",
#                         "High",
#                         "Low",
#                         "Close",
#                         'Volume',
#                         "Closetime",
#                         "Assetvol",
#                         "Numberoftrades",
#                         "Takerbuybase",
#                         "Takerbuyquote",
#                         "Ignore",
#                     ])



# data.set_index('Opentime', inplace=True)
# data.index = pd.to_datetime(data.index, unit='ms')

# btalib.config.set_return_dataframe()  # force return of a DataFrame

# my_sma = btalib.sma(data)

# print(data)
# print(data.Close)
# print(btalib.rsi(data.Close))


cerebro.adddata(data)

cerebro.addstrategy(RSIStrategy)

cerebro.run()

cerebro.plot()
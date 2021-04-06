import backtrader
import datetime

from bullish_engulfing_strategy import Engulfingstrategy
from strategies import TestStrategy

homeboy = backtrader.Cerebro()

homeboy.broker.set_cash(100000)

data = backtrader.feeds.GenericCSVData(dataname='2020_5m.csv', dtformat=2, compression=5, timeframe=backtrader.TimeFrame.Minutes)

# data = backtrader.feeds.GenericCSVData(
#     dataname='2021_Jan_5m.csv',
#     nullvalue=0.0,
#     dtformat=2,
#     datetime=0,
#     open=1,
#     high=2,
#     low=3,
#     close=4,
#     volume=5,
#     Closedate=6,
#     Assetvol=7,
#     NOT=8,
#     TBB=9,
#     TBQ=10,
#     Ignore=-1,
#     compression=5,
#     timeframe=backtrader.TimeFrame.Minutes
# )

homeboy.adddata(data)

#homeboy.addstrategy(TestStrategy)
homeboy.addstrategy(Engulfingstrategy)

print('Starting Portfolio Value: %.2f' % homeboy.broker.getvalue())

homeboy.run()

print('Finaleee Portfolio Value: %.2f' % homeboy.broker.getvalue())

homeboy.plot()



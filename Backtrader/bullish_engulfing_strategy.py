import backtrader as bt
import datetime as datetime1
from datetime import datetime
from dateutil import tz


# Strategie aufbauen
def _from_ordinal(x):
    ix = int(x)
    dt = datetime1.date.fromordinal(ix)
    remainder = float(x) - ix
    hour, remainder = divmod(24 * remainder, 1)
    minute, remainder = divmod(60 * remainder, 1)
    second, remainder = divmod(60 * remainder, 1)
    dt = datetime1.datetime(dt.year, dt.month, dt.day, int(hour), int(minute), int(second))
    dt = dt.isoformat()

    dt = dt.replace('T', ' ')

    utc = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc = utc.replace(tzinfo=from_zone)

    local = utc.astimezone(to_zone)

    return local.strftime('%m.%d.%Y %H:%M:%S')


# Prüfen ob Candle Bearish ist
def is_bearish_candlestick(candle_open_prev, candle_close_prev):
    return candle_open_prev > candle_close_prev


# Prüfen ob es ein Engulfing Pattern ist
def is_bullish_engulfing(candle_open_prev, candle_close_prev, candle_open_curr, candle_close_curr):
    if is_bearish_candlestick(candle_open_prev, candle_close_prev) \
            and candle_close_curr > candle_open_prev \
            and candle_open_curr <= candle_close_prev:
        return True

    return False


def is_bullish_candlestick(candle_open_prev, candle_close_prev):
    return candle_open_prev < candle_close_prev


def is_bearish_engulfing(candle_open_prev, candle_close_prev, candle_open_curr, candle_close_curr):
    if is_bearish_candlestick(candle_open_prev, candle_close_prev) \
            and candle_close_curr < candle_open_prev \
            and candle_open_curr >= candle_close_prev:
        return True

    return False


# Zeitumwandlungsmethode
# Engulfingstrategy aufbauen
class Engulfingstrategy(bt.Strategy):

    def log(self, txt, dt=None):
        # Logging der Strategie
        # dt = dt or self.convert_timestamp(self.datas[0].datetime())
        dt = dt or _from_ordinal(self.datas[0].datetime[0])
        print('%s, %s' % (dt, txt))

    def __init__(self):
        self.candle = self.datas[0]
        self.order = None
        self.TPs = 0
        self.SLs = 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
                self.bull_engulf_bear_close = self.datas[0].low[-2]
                self.execution_price_BULL = order.executed.price
                self.SL_BULL = self.bull_engulf_bear_close - 10
                self.difference_bull = self.execution_price_BULL - self.SL_BULL
                self.TP_BULL = self.execution_price_BULL + self.difference_bull + self.difference_bull
                self.BULL = True
            elif order.issell():
                self.log('CLOSE EXECUTED {}'.format(order.executed.price))
                # self.bear_engulf_bull_close = self.datas[0].close[-2]
                # self.execution_price_BEAR = order.executed.price
                # self.SL_BEAR = self.bear_engulf_bull_close + 10
                # self.difference_bear = self.SL_BEAR - self.execution_price_BEAR
                # self.TP_BEAR = self.execution_price_BEAR - self.difference_bear - self.difference_bear
                # self.BEAR = True
        self.order = None

    def next(self):
        self.log('Close, %.2f' % self.candle.close[0], _from_ordinal(self.candle.datetime[0]))

        if self.order:
            return

        if not self.position:
            if is_bullish_engulfing(self.candle.open[-1], self.candle.close[-1], self.candle.open[0],
                                    self.candle.close[0]):
                print("Bullish Engulfing @ " + _from_ordinal(self.candle.datetime[0]))
                self.buy(size=2)

            # if is_bearish_engulfing(self.candle.open[-1], self.candle.close[-1], self.candle.open[0], self.candle.close[0]):
            #   print("Bearish Engulfing @ " + _from_ordinal(self.candle.datetime[0]))
            #  self.sell(size=0.03)
        else:
            if self.candle.close[0] < self.SL_BULL:
                self.SLs = self.SLs + 1
                print("STOP-LOSS @ " + _from_ordinal(self.candle.datetime[0]))
                print(self.SLs)
                self.order = self.close(size=2)
            if self.candle.close[0] > self.TP_BULL:
                self.TPs = self.TPs + 1
                print("TAKE-PROFIT @ " + _from_ordinal(self.candle.datetime[0]))
                print(self.TPs)
                self.order = self.close(size=2)

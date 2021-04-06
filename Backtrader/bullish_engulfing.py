import csv
from datetime import datetime
from dateutil import tz


def convert_timestamp(ts):
    ts = float(ts)
    dt = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    utc = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc = utc.replace(tzinfo=from_zone)

    local = utc.astimezone(to_zone)

    return local.strftime('%m.%d.%Y %H:%M:%S')


def is_bearish_candlestick(candle):
    return candle['Close'] < candle['Open']


def is_bullish_engulfing(candles, index):
    current_day = candles[index]
    previous_day = candles[index - 1]

    if is_bearish_candlestick(previous_day) \
            and current_day['Close'] > previous_day['Open'] \
            and current_day['Open'] <= previous_day['Close']:
        return True

    return False


with open('2021_Jan_5m.csv') as data:
    reader = csv.DictReader(data)
    candles = list(reader)

for i in range(1, len(candles)):
    print(candles[i])

    if is_bullish_engulfing(candles, i):
        print("Bullish Engulfing at", convert_timestamp(candles[i]['Date']))


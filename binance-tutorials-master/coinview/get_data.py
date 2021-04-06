import config
import csv
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

# preis = client.get_all_tickers()

# for price in preis:
#    print(price)

csvdata = open('2020_5m_excel.csv', 'w', newline='')
candlestick_writer = csv.writer(csvdata, delimiter=';')

candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_5MINUTE, "1 Jan, 2020", "10 Jan, 2020")
# candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2020", "12 Jul, 2020")
# candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2017", "12 Jul, 2020")

for candlestick in candlesticks:
    candlestick[0] = candlestick[0] / 1000
    candlestick_writer.writerow(candlestick)

csvdata.close()

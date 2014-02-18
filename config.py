MONGO_SERVER = 'localhost'
MONGO_DB = 'coinstalk'
WEB_PORT = 8092

URLS = [
  ['mtgox', 'http://data.mtgox.com/api/2/BTCUSD/money/ticker_fast'],
  ['bitstamp', 'https://www.bitstamp.net/api/ticker/'],
  ['btc-e', 'https://btc-e.com/api/2/btc_usd/ticker'],
  ['bitfinex', 'https://api.bitfinex.com/v1/ticker/btcusd'],
]

TIME_RANGE = {
  '3hr': 60 * 60 * 3,
  '24hr': 60 * 60 * 24,
  '7d' : 60 * 60 * 24 * 7,
  '30d': 60 * 60 * 24 * 30,
}

SAMPLING_RATE = {
  '3hr' : 180,
  '24hr' : 288,
  '7d' : 336,
  '30d' : 336,
}


import eventlet
import logging
import json
from datetime import datetime
from pymongo import MongoClient
from eventlet.green import urllib2

import config

def fetch(url):
  content = urllib2.urlopen(url[1]).read()
  return (url[0], content)

def record(parser, content):
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  d = json.loads(content)
  result = dict()
  if parser == 'mtgox':
    result['trader'] = 'mtgox'
    print int(d['data']['now'])
    result['timestamp'] = datetime.fromtimestamp(int(d['data']['now']) / 1e6)
    last_s = d['data']['last_local']['display'].split('$')[1]
    result['last'] = float(last_s)
    conn.value.insert(result)
  elif parser == 'bitstamp':
    result['trader'] = 'bitstamp'
    result['timestamp'] = datetime.fromtimestamp(int(d['timestamp']))
    result['last'] = float(d['last'])
    result['high'] = float(d['high'])
    result['bid'] = float(d['bid'])
    result['volume'] = float(d['volume'])
    result['low'] = float(d['low'])
    result['ask'] = float(d['ask'])
    conn.value.insert(result)
  elif parser == 'btc-e':
    result['trader'] = 'btc-e'
    d = d['ticker']
    result['timestamp'] = datetime.fromtimestamp(int(d['updated']))
    result['last'] = float(d['last'])
    result['high'] = float(d['high'])
    result['volume'] = float(d['vol_cur'])
    result['low'] = float(d['low'])
    conn.value.insert(result)
  elif parser == 'bitfinex':
    result['trader'] = 'bitfinex'
    result['timestamp'] = datetime.fromtimestamp(round(float(d['timestamp'])))
    result['last'] = float(d['last_price'])
    result['mid'] = float(d['mid'])
    result['ask'] = float(d['ask'])
    conn.value.insert(result)
    pass
  else:
    logging.error('invalid parser: '+ parser)
    return 0

if __name__ == '__main__':
  pool = eventlet.GreenPool()
  for body in pool.imap(fetch, config.URLS):
    record(body[0], body[1])


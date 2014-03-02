import bottle
import json
import datetime
import time
import logging
from bottle import get, post, route, run, hook, response, request, template
from pymongo import MongoClient

import config

def sampling(rows, count, rate):
  result = {}
  values = []
  high = 0.0
  low = 9999999.0
  step_size = count / rate
  c = 0
  for i,row in enumerate(rows):
    if i == 0:
      result['first'] = row['last']
    if c <= 0:
      c += step_size
      values.append(row['last'])
    c -= 1
    result['last'] = row['last']
    result['timestamp'] = time.mktime(row['timestamp'].timetuple())
    if result['last'] > high:
      high = result['last']
    if result['last'] < low:
      low = result['last']
  result['high'] = high
  result['low'] = low
  result['values'] = values
  result['change'] = (result['last'] - result['first'])*100 / result['last']
  return result 

def query_values(trader, time_range_str, time_end):
  values = []
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  sampling_rate = config.SAMPLING_RATE[time_range_str]
  time_range = config.TIME_RANGE[time_range_str]
  time_start = time_end - datetime.timedelta(seconds=time_range)
  logging.error("time_start" +str(time_start))
  logging.error("time_end" +str(time_end))
  query = {
    'trader': trader,
    'timestamp' : { '$gt' : time_start, '$lte': time_end},
  }
  rows = conn.value.find(query)
  count = rows.count()
  logging.error("count: " +str(count))
  values = sampling(rows, count, sampling_rate)
  return values

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@get('/')
def view_root():
  return {'hello': 'coinstalk'}

@get('/api/values/<trader>/<time_range>')
def api_values(trader, time_range):
  time_end = datetime.datetime.now()
  values = query_values(trader, time_range, time_end)
  return {'values' : values}


if __name__ == '__main__':
  run (host='0.0.0.0', port=config.WEB_PORT, debug=True,reloader=True)


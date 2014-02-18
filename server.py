import bottle
import json
import datetime
from bottle import get, post, route, run, request, template
from pymongo import MongoClient

import config


@get('/')
def view_root():
  return {'hello': 'coinstalk'}

@get('/api/query/<trader>/<time>')
def api_query():



if __name__ == '__main__':
  run (host='0.0.0.0', port=config.WEB_PORT, debug=True,reloader=True)


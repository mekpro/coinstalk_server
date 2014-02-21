from pymongo import MongoClient

import config

if __name__ == '__main__':
  conn = MongoClient(config.MONGO_SERVER)[config.MONGO_DB]
  conn.last_update.insert({'last_update':datetime.datetime.now()})
  conn.value.ensureIndex({trader:1, timestamp:1})

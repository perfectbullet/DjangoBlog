from pymongo import MongoClient
from urllib.parse import quote_plus

uri = "mongodb://%s:%s@%s" % (quote_plus('admin'), quote_plus('123456'), '49.232.208.236')
client = MongoClient(uri)

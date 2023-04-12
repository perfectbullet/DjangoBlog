from mongo_db import client
from gridfs import GridFS
from bson.objectid import ObjectId


db = client.school
gfs = GridFS(db, collection='book')
gfs.delete(ObjectId('6434077730dc30cbd241b528'))

from mongo_db import client
from gridfs import GridFS
from bson.objectid import ObjectId


db = client.school
gfs = GridFS(db, collection='book')
document = gfs.get(ObjectId('6434077730dc30cbd241b528'))
file = open('D:/Python 手册.pdf', 'wb')
file.write(document.read())
file.close()

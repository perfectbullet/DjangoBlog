from mongo_db import client
from gridfs import GridFS


db = client.school
gfs = GridFS(db, collection='book')

file = open('D:/Python 编码规范.pdf', 'rb')
args = {'type': 'PDF', 'keyword': 'Python'}
gfs.put(file, filename='Python 编码规范', **args)
file.close()

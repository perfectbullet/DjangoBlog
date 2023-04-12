import math
import datetime
from mongo_db import client
from gridfs import GridFS
from bson.objectid import ObjectId


db = client.school
gfs = GridFS(db, collection='book')
book = gfs.find_one({'filename': 'Python 编码规范'})
print(book.filename)
print(book.type)
print(book.keyword)
print('%dM' % math.ceil(book.length/1024/1024))
print('----------------')
books = gfs.find({'type': 'PDF'})
for one in books:
    uploadDate = one.uploadDate + datetime.timedelta(hours=8)
    uploadDate = uploadDate.strftime('%Y-%m-%d %H:%M:%S')
    print(one._id, one.filename, uploadDate)
print('-----------------')
rs = gfs.exists(ObjectId('6434077730dc30cbd241b528'))
print(rs)
rs = gfs.exists(**{'type': 'PDF'})
print(rs)

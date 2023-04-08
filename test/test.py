import pymongo
from pymongo import MongoClient
import urllib.parse

if __name__ == '__main__':





    username = urllib.parse.quote_plus('admin')

    password = urllib.parse.quote_plus('123456')
    myclient = MongoClient('mongodb://%s:%s@49.232.208.236' % (username, password))
    # myclient = pymongo.MongoClient("mongodb://49.232.208.236:27017/")
    mydb = myclient["runoobdb222"]

    document1 = {'zhoujing': 2222222222}

    posts = mydb.posts  # 你也可以不这样做，每次通过db.posts调用
    post_1 = posts.insert_one(document1).inserted_id

    for data in posts.find():
        print(data)
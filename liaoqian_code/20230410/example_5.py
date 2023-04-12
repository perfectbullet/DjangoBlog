from mongo_db import client


students = client.school.student.find({}).skip(0).limit(10)
for one in students:
    print(one['_id'], one['name'])

names = client.school.student.distinct('name')
for one in names:
    print(one)

students = client.school.student.find({}).sort([('name', -1)])
for one in students:
    print(one['_id'], one['name'])
    
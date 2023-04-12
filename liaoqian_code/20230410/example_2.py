from mongo_db import client


try:
    teachers = client.school.teacher.find({})
    for one in teachers:
        print(one['_id'], one['name'])
    print('----------------------------')
    teacher = client.school.teacher.find_one({'name': '李璐'})
    print(teacher['_id'], teacher['name'])
except Exception as e:
    print(e)

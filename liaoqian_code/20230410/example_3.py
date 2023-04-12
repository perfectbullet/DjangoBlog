from mongo_db import client


try:
    client.school.teacher.update_many({}, {'$set': {'role': ['班主任']}})
    client.school.teacher.update_one({'name': '李璐'}, {'$set': {'sex': '女'}})
    client.school.teacher.update_one({'name': '李璐'},
                                     {'$push': {'role': '年级主任'}})
except Exception as e:
    print(e)

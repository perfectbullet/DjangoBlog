# coding:utf-8

'''
   学生信息库
'''

students = {
    1: {
        'name': 'dewei',
        'age': 33,
        'class_number': 'A',
        'sex': 'boy'
    },
    2: {
        'name': '小慕',
        'age': 10,
        'class_number': 'B',
        'sex': 'boy'
    },
    3: {
        'name': '小曼',
        'age': 18,
        'class_number': 'A',
        'sex': 'girl'
    },
    4: {
        'name': '小高',
        'age': 18,
        'class_number': 'C',
        'sex': 'boy'
    },
    5: {
        'name': '小云',
        'age': 18,
        'class_number': 'B',
        'sex': 'girl'
    }
}


def check_user_info(**kwargs):
    if 'name' not in kwargs:
        return '没有发现学生姓名'
    if 'age' not in kwargs:
        return '缺少学生年龄'
    if 'sex' not in kwargs:
        return '缺少学生性别'
    if 'class_number' not in kwargs:
        return '缺少学生班级'
    return True


def get_all_students():
    for id_, value in students.items():
        print('学号:{}, 姓名{}， 年龄：{}， 性别：{}， 班级：{}'.format(
            id_, value['name'], value['age'], value['sex'], value['class_number']
        ))
    return students


# result = get_all_students()
# print('-----', result)


def add_students(**kwargs):
    check = check_user_info(**kwargs)
    if check != True:
        print(check)
        return

    id_ = max(students) + 1

    students[id_] = {
        'name': kwargs['name'],
        'age': kwargs['age'],
        'sex': kwargs['sex'],
        'class_number': kwargs['class_number']
    }


# add_students(name='小白', age=19, class_number='A', sex='boy')
# get_all_students()

def delete_students(students_id):
    if students_id not in students:
        print('{}并不存在'.format(students_id))
    else:
        user_info = students.pop(students_id)
        print('学号是{}, {}同学的信息已经被删除了'.format(students_id, user_info['name']))


# delete_students(1)
# add_students(name='小白', age=19, class_number='A', sex='boy')
# get_all_students()


def update_students(students_id, **kwargs):
    if students_id not in students:
        print('并不存在这个学号：{}'.format(students_id))

    check = check_user_info(**kwargs)
    if check != True:
        print(check)
        return

    students[students_id] = kwargs
    print('同学信息更新完毕')


update_students(1, name='dewei.zhang', age=33, class_number='A', sex='boy')
get_all_students()


def get_user_by_id(students_id):
    return students.get(students_id)


print(get_user_by_id(3))


def search_users(**kwargs):
    values = list(students.values())
    key = None
    value = None
    result = []

    if 'name' in kwargs:
        key = 'name'
        value = kwargs[key]
    elif 'sex' in kwargs:
        key = 'sex'
        value = kwargs[key]
    elif 'class_number' in kwargs:
        key = 'class_number'
        value = kwargs[key]
    elif 'age' in kwargs:
        key = 'age'
        value = kwargs[key]
    else:
        print('没有发现搜索的关键字')
        return

    for user in values:
        if user[key] == value:
            result.append(user)
    return result


print('-----')
users = search_users(sex='girl')
print(users)

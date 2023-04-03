# coding:utf-8

f = lambda: print(1)
f()

f1 = lambda x, y=2: x > y
print(f1(1))


users = [
    {'name': 'dewei'},
    {'name': 'xiaomu'},
    {'name': 'asan'}
]
users.sort(key=lambda x: x['name'])
print(users)
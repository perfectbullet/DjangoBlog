# coding:utf-8

books = []
print(id(books))
books.append('python入门课程')
print(books)
print(id(books))

number = 1.1
tuple_tset = (1,)
dict_test = {'name': 'dewei'}

books.append(number)
books.append(tuple_tset)
books.append(dict_test)

print(books)
print(id(books))

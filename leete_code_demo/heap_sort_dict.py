# 字典堆排序
import random


def heap_sort_dict(my_dict):
    group_of_key_value = [[key, value] for key, value in my_dict.items()]
    print('group_of_key_value ')
    print(group_of_key_value)
    # array = [new_dict.keys()]  # 键的值组成新数组去做堆排序    对list操作不熟悉
    array = group_of_key_value
    first = len(array) // 2 - 1
    for start in range(first, -1, -1):
        big_heap(array, start, len(array) - 1)
    for end in range(len(array) - 1, 0, -1):
        array[0], array[end] = array[end], array[0]
        big_heap(array, 0, end - 1)
    sorted_dic = {key: value for key, value in array}
    return sorted_dic


def big_heap(array, start, end):
    root = start
    child = root * 2 + 1
    # array[child][1] 每个分组中， 第二个元素是值
    while child <= end:
        if child + 1 <= end and array[child][1] < array[child + 1][1]:
            child += 1
        if array[root][1] < array[child][1]:
            array[root][1], array[child][1] = array[child][1], array[root][1]
            root = child
            child = root * 2 + 1
        else:
            break


if __name__ == '__main__':
    array = [10, 17, 50, 7, 30, 24, 27, 45, 15, 5, 36, 21]
    my_dict = {'{}'.format(random.randint(100, 200)): i for i in array}
    print(heap_sort_dict(my_dict))


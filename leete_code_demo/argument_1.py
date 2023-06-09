"""
@FileName：argument_1.py\n
@Description：\n
@Author：zhoujing\n
@contact：121531845@qq.com\n
@Time：2023/6/9 20:32\n
@Department：红石扩大小区\n
@Website：www.zhoujing.com\n
@Copyright：©2019-2023 xxx信息科技有限公司
"""

def permutations(iterable, r=None):
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n-r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i+1:] + indices[i:i+1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def solution(arr: list):
    """
    @param arr:
    @return:
    """
    arr_str = [str(i) for i in arr]
    big_number = ''.join(arr_str)
    # permutations 直接计算排列数，然后直接比较字符串大小
    for e in permutations(arr_str):
        a_number = ''.join(e)
        if a_number > big_number:
            big_number = a_number
    return big_number


if __name__ == '__main__':
    # 一个列表【11，52，5，6，511】，将其中的元素组成最大的数
    arr = [11, 52, 5, 6, 511]
    anwser = solution(arr)
    print(anwser)

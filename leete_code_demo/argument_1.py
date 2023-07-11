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


def permutations(iterable):
    """
    @param iterable:
    @param r:
    @return:
    """
    pool = tuple(iterable)
    n = len(pool)

    indices = list(range(n))
    cycles = list(range(n, n - n, -1))
    yield tuple(pool[ii] for ii in indices[:n])
    while n:
        for k in reversed(range(n)):
            cycles[k] -= 1
            if cycles[k] == 0:
                indices[k:] = indices[k + 1:] + indices[k:k + 1]
                cycles[k] = n - k
            else:
                j = cycles[k]
                indices[k], indices[-j] = indices[-j], indices[k]
                print('cycles ', cycles)
                print('indices ', indices)
                print('====================')
                yield tuple(pool[i2] for i2 in indices)
                break
        else:
            return


def permutations2(arr):
    # 1.如果输入的序列长度小于等于1，则直接返回该序列。
    # 2.否则，初始化结果集合res为空
    # 3.遍历序列arr中的每个元素ch和其对应的索引值i，将ch从arr中移除，得到剩余的子序列 arr[:i] + arr[i+1:]
    # 4.对剩余子序列调用递归函数permutations，得到子序列所有的全排列，并循环将ch插入到每个全排列的每个位置上，添加到结果集res中
    # 5.返回结果集res。
    if len(arr) <= 1:
        return [arr]
    else:
        res = []
        for i, ch in enumerate(arr):
            for j in permutations2(arr[:i] + arr[i + 1:]):
                res.append([ch] + j)
        return res


def solution(arr: list):
    """
    @param arr:
    @return:
    """
    arr_str = [str(i) for i in arr]
    big_number = ''.join(arr_str)
    # permutations 直接计算排列数，然后直接比较字符串大小
    for e in permutations3(arr_str):
        a_number = ''.join(e)
        # print(a_number)
        if a_number > big_number:
            big_number = a_number
    return big_number


def permutations3(iterable):
    # 还是计算所有组合
    pool = tuple(iterable)
    n = len(pool)
    # 通过 product 把所有下表的排列计算出来
    for indices in product(range(n), repeat=n):
        if len(set(indices)) == n:
            yield tuple(pool[i] for i in indices)


def product(idxs, repeat=1):
    # 按组合数的个数
    pools = [tuple(idxs), ] * repeat
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)


if __name__ == '__main__':
    # 一个列表【11，52，5，6，511】，将其中的元素组成最大的数
    arr = [11, 52, 5, 6, 511]
    anwser = solution(arr)
    print(anwser)
    # t = product(range(len(arr)), repeat=len(arr))
    # print(list(t))

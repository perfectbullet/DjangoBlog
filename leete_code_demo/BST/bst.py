"""
@FileName：bst.py
@Description：
二叉树python 示例
@Author：zhoujing
@contact：121531845@qq.com
@Time：2023/7/14 23:20
@Department：红石扩大小区
@Website：www.zhoujing.com
@Copyright：©2019-2023 xxx信息科技有限公司
"""


# 二叉搜索树（BST）是二叉树的一种特殊表示形式，它满足如下特性：
#
# 每个节点中的值必须大于（或等于）存储在其左侧子树中的任何值。
# 每个节点中的值必须小于（或等于）存储在其右子树中的任何值。
#
# 链接：https://leetcode.cn/leetbook/read/introduction-to-data-structure-binary-search-tree/xp6fkc/


class BSTNode:
    """
    二叉树的节点
    """

    def __init__(self, val):
        # 节点值
        self.val = val
        # 左节点, BinaryTreeNode 或者 None
        self.left = None
        # 右节点, BinaryTreeNode 或者 None
        self.right = None

    def insert(self, val):
        # 给 bst 新增一个值
        # 新增值就要看值
        if not self.val:
            self.val = val
            return
        if self.val == val:
            # 等于的情况，值就在二叉树中，不用插入
            return
        if val < self.val:
            # 比当前节点值小，按定义， 要放到左边子节点
            if self.left is not None:
                # 左边子节点不为空
                self.left.insert(val)
            else:
                # 左子节点为空, 那么就给左子节点新建一个
                self.left = BSTNode(val)
        else:
            # 比当前节点值大，按定义， 要放到右边子节点
            if self.right is not None:
                self.right.insert(val)
            else:
                self.right = BSTNode(val)

    def search(self, val):
        if val == self.val:
            return True

        if val < self.val:
            if self.left is None:
                return False
            return self.left.search(val)

        if self.right is None:
            return False
        return self.right.search(val)


if __name__ == '__main__':
    bst = BSTNode(52)
    bst.insert(50)
    bst.insert(20)
    bst.insert(53)
    bst.insert(11)
    bst.insert(22)
    bst.insert(52)
    bst.insert(78)

    print("53 is present in the binary tree:", bst.search(53))
    print("100 is present in the binary tree:", bst.search(100))

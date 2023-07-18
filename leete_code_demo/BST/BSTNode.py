class BSTNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def insert(self, val):
        if not self.val:
            self.val = val
            return
        if self.val == val:
            return
        if val < self.val:
            if self.left is not None:
                self.left.insert(val)
            else:
                self.left = BSTNode(val)
        else:
            if self.right is not None:
                self.right.insert(val)
            else:
                self.right = BSTNode(val)


class Solution:
    def inorderTraversal(self, root):
        result = []
        self.accessTree(root, result)
        return result

    def accessTree(self, root, result):
        if root == None:
            return
        self.accessTree(root.left, result)
        result.append(root.val)
        self.accessTree(root.right, result)


if __name__ == '__main__':
    BST = BSTNode(5)
    BST.insert(7)
    BST.insert(6)
    BST.insert(3)
    BST.insert(3)
    BST.insert(2)
    BST.insert(1)
    res = Solution().inorderTraversal(BST)
    print(res)



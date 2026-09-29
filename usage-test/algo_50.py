"""Binary search tree (BST).

Each node's left subtree holds smaller keys and right subtree larger
keys. Supports insert, search, delete (with in-order successor), in-order
traversal, height, min/max, and validation.
Time: O(h) per operation, h = tree height (O(log n) if balanced).
"""


class Node:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None


class BST:
    def __init__(self, keys=()):
        self.root = None
        for k in keys:
            self.insert(k)

    def insert(self, key):
        def _ins(node):
            if node is None:
                return Node(key)
            if key < node.key:
                node.left = _ins(node.left)
            elif key > node.key:
                node.right = _ins(node.right)
            return node
        self.root = _ins(self.root)

    def contains(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def delete(self, key):
        def _del(node, key):
            if node is None:
                return None
            if key < node.key:
                node.left = _del(node.left, key)
            elif key > node.key:
                node.right = _del(node.right, key)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.key = succ.key
                node.right = _del(node.right, succ.key)
            return node
        self.root = _del(self.root, key)

    def inorder(self):
        out = []

        def walk(n):
            if n:
                walk(n.left)
                out.append(n.key)
                walk(n.right)
        walk(self.root)
        return out

    def height(self):
        def h(n):
            return 0 if n is None else 1 + max(h(n.left), h(n.right))
        return h(self.root)

    def is_valid(self):
        def ok(n, lo, hi):
            if n is None:
                return True
            if not (lo < n.key < hi):
                return False
            return ok(n.left, lo, n.key) and ok(n.right, n.key, hi)
        return ok(self.root, float("-inf"), float("inf"))


if __name__ == "__main__":
    t = BST([50, 30, 70, 20, 40, 60, 80])
    assert t.inorder() == [20, 30, 40, 50, 60, 70, 80]
    assert t.contains(60) and not t.contains(65)
    assert t.height() == 3 and t.is_valid()
    t.delete(20)   # leaf
    t.delete(30)   # one child
    t.delete(50)   # two children (root)
    assert t.inorder() == [40, 60, 70, 80]
    assert t.root.key == 60 and t.is_valid()
    t.insert(60)   # duplicate ignored
    assert t.inorder() == [40, 60, 70, 80]
    assert BST(range(5)).height() == 5
    print("algo_50 binary search tree: all tests passed")

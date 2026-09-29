"""Segment tree with range-sum queries and point updates.

A complete binary tree over the array stored iteratively (size 2n):
leaves are the elements, each internal node is the sum of its children.
Also a generic version parameterised by an associative operation
(demonstrated with min).
Time: O(log n) query and update, O(n) build. Space: O(n).
"""


class SegmentTree:
    def __init__(self, data, op=lambda a, b: a + b, identity=0):
        self.n = len(data)
        self.op = op
        self.identity = identity
        self.tree = [identity] * self.n + list(data)
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = op(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, idx, value):
        """Set data[idx] = value."""
        i = idx + self.n
        self.tree[i] = value
        while i > 1:
            i //= 2
            self.tree[i] = self.op(self.tree[2 * i], self.tree[2 * i + 1])

    def query(self, lo, hi):
        """Aggregate over the half-open range [lo, hi)."""
        left_res, right_res = self.identity, self.identity
        lo += self.n
        hi += self.n
        while lo < hi:
            if lo & 1:
                left_res = self.op(left_res, self.tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                right_res = self.op(self.tree[hi], right_res)
            lo //= 2
            hi //= 2
        return self.op(left_res, right_res)


if __name__ == "__main__":
    data = [2, 1, 5, 3, 4, 7, 6]
    st = SegmentTree(data)
    for i in range(len(data)):
        for j in range(i, len(data) + 1):
            assert st.query(i, j) == sum(data[i:j])
    st.update(2, 10)
    data[2] = 10
    assert st.query(0, 7) == sum(data)
    assert st.query(2, 3) == 10
    mt = SegmentTree(data, op=min, identity=float("inf"))
    assert mt.query(0, 7) == 1
    assert mt.query(2, 5) == 3
    mt.update(1, 50)
    assert mt.query(0, 3) == 2
    # Non-commutative op (string concatenation) keeps order.
    ct = SegmentTree(list("abcdef"), op=lambda a, b: a + b, identity="")
    assert ct.query(1, 5) == "bcde"
    print("algo_53 segment tree: all tests passed")

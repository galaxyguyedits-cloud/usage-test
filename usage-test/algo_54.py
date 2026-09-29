"""Fenwick tree (binary indexed tree).

Stores partial sums so that prefix sums and point updates both take
O(log n) by walking indices with i += i & -i (update) and i -= i & -i
(query). Also supports range sums and finding the smallest index with a
given prefix sum (lower bound) for non-negative values.
Space: O(n).
"""


class FenwickTree:
    def __init__(self, n_or_data):
        if isinstance(n_or_data, int):
            self.n = n_or_data
            self.tree = [0] * (self.n + 1)
        else:
            data = list(n_or_data)
            self.n = len(data)
            self.tree = [0] + data
            # O(n) construction.
            for i in range(1, self.n + 1):
                j = i + (i & -i)
                if j <= self.n:
                    self.tree[j] += self.tree[i]

    def add(self, idx, delta):
        """data[idx] += delta (0-indexed)."""
        i = idx + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, idx):
        """Sum of data[0:idx]."""
        total, i = 0, idx
        while i > 0:
            total += self.tree[i]
            i -= i & -i
        return total

    def range_sum(self, lo, hi):
        """Sum of data[lo:hi]."""
        return self.prefix_sum(hi) - self.prefix_sum(lo)

    def lower_bound(self, target):
        """Smallest idx such that prefix_sum(idx + 1) >= target."""
        pos, step = 0, 1 << self.n.bit_length()
        while step:
            if pos + step <= self.n and self.tree[pos + step] < target:
                pos += step
                target -= self.tree[pos]
            step >>= 1
        return pos


if __name__ == "__main__":
    data = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    ft = FenwickTree(data)
    for i in range(len(data) + 1):
        assert ft.prefix_sum(i) == sum(data[:i])
    assert ft.range_sum(3, 7) == 12
    ft.add(2, 5)
    data[2] += 5
    assert ft.range_sum(0, 11) == sum(data)
    empty = FenwickTree(5)
    for i, v in enumerate([1, 1, 1, 1, 1]):
        empty.add(i, v)
    assert empty.prefix_sum(5) == 5
    counts = FenwickTree([2, 0, 3, 1])
    assert counts.lower_bound(1) == 0
    assert counts.lower_bound(3) == 2
    assert counts.lower_bound(6) == 3
    print("algo_54 Fenwick tree: all tests passed")

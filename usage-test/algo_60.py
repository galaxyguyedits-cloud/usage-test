"""Subsets (power set) and combinations.

- power set via bitmasks: subset i contains element j iff bit j of i
- power set via backtracking (lexicographic by index)
- k-combinations via backtracking with pruning
- subset-sum decision/enumeration via include/exclude recursion
- Gray-code ordering where consecutive subsets differ by one element.
Time: O(2^n * n). Space: O(n) recursion.
"""


def power_set_bits(items):
    n = len(items)
    return [[items[j] for j in range(n) if i >> j & 1] for i in range(1 << n)]


def power_set_backtrack(items):
    out, cur = [], []

    def go(start):
        out.append(list(cur))
        for i in range(start, len(items)):
            cur.append(items[i])
            go(i + 1)
            cur.pop()

    go(0)
    return out


def combinations(items, k):
    out, cur = [], []

    def go(start):
        if len(cur) == k:
            out.append(list(cur))
            return
        # Prune: not enough elements left to reach size k.
        for i in range(start, len(items) - (k - len(cur)) + 1):
            cur.append(items[i])
            go(i + 1)
            cur.pop()

    go(0)
    return out


def subset_sums(nums, target):
    """Return all index-ordered subsets of nums summing to target."""
    res = []

    def go(i, cur, total):
        if i == len(nums):
            if total == target:
                res.append(list(cur))
            return
        cur.append(nums[i])
        go(i + 1, cur, total + nums[i])
        cur.pop()
        go(i + 1, cur, total)

    go(0, [], 0)
    return res


def gray_code(n):
    return [i ^ (i >> 1) for i in range(1 << n)]


if __name__ == "__main__":
    from itertools import combinations as it_comb

    ps = power_set_bits([1, 2, 3])
    assert len(ps) == 8 and [] in ps and [1, 2, 3] in ps
    bt = power_set_backtrack([1, 2, 3])
    assert sorted(map(tuple, bt)) == sorted(map(tuple, ps))
    assert bt[:4] == [[], [1], [1, 2], [1, 2, 3]]
    for k in range(5):
        assert combinations("abcd", k) == [list(c) for c in it_comb("abcd", k)]
    assert sorted(subset_sums([3, 34, 4, 12, 5, 2], 9)) == [[3, 4, 2], [4, 5]]
    g = gray_code(3)
    assert g == [0, 1, 3, 2, 6, 7, 5, 4]
    assert all(bin(a ^ b).count("1") == 1 for a, b in zip(g, g[1:]))
    print("algo_60 subsets and combinations: all tests passed")

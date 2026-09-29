"""Longest increasing subsequence (LIS).

Two approaches: the O(n^2) DP where dp[i] is the LIS ending at i, and
the O(n log n) patience-sorting method that maintains the smallest tail
of every increasing subsequence length, with parent pointers so the
actual subsequence can be reconstructed.
"""

from bisect import bisect_left


def lis_quadratic(arr):
    """Length of the strictly increasing LIS in O(n^2)."""
    if not arr:
        return 0
    dp = [1] * len(arr)
    for i in range(len(arr)):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def lis(arr):
    """Return one strictly increasing subsequence of maximum length."""
    tails = []        # tails[k] = value ending the best length-(k+1) run
    tails_idx = []    # index in arr of tails[k]
    parent = [-1] * len(arr)
    for i, x in enumerate(arr):
        k = bisect_left(tails, x)
        if k == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[k] = x
            tails_idx[k] = i
        parent[i] = tails_idx[k - 1] if k > 0 else -1
    out = []
    i = tails_idx[-1] if tails_idx else -1
    while i != -1:
        out.append(arr[i])
        i = parent[i]
    return out[::-1]


def is_strictly_increasing(seq):
    return all(a < b for a, b in zip(seq, seq[1:]))


if __name__ == "__main__":
    data = [10, 9, 2, 5, 3, 7, 101, 18]
    assert lis_quadratic(data) == 4
    res = lis(data)
    assert len(res) == 4 and is_strictly_increasing(res)
    assert lis([]) == []
    assert lis([5, 5, 5]) == [5]
    assert lis([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]) and \
        len(lis([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15])) == 6
    for seq in ([3, 1, 2], [1, 2, 3, 4], [4, 3, 2, 1], [2, 6, 3, 4, 1, 2, 9]):
        assert len(lis(seq)) == lis_quadratic(seq)
    print("algo_36 LIS: all tests passed")

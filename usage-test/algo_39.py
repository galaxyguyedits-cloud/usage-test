"""Matrix chain multiplication.

Given dimensions p[0..n] for matrices A1 (p0 x p1) ... An (p[n-1] x pn),
find the parenthesisation minimising scalar multiplications. Interval DP
over chain lengths with a split table for reconstruction.
Time: O(n^3). Space: O(n^2).
"""


def matrix_chain_order(p):
    """Return (min_cost, split) tables for dimension list p."""
    n = len(p) - 1
    cost = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float("inf")
            for k in range(i, j):
                q = cost[i][k] + cost[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                if q < cost[i][j]:
                    cost[i][j] = q
                    split[i][j] = k
    return cost, split


def parenthesize(split, i, j):
    """Return optimal parenthesisation string for matrices i..j."""
    if i == j:
        return f"A{i + 1}"
    k = split[i][j]
    return f"({parenthesize(split, i, k)}{parenthesize(split, k + 1, j)})"


def min_multiplications(p):
    if len(p) < 3:
        return 0
    cost, _ = matrix_chain_order(p)
    return cost[0][-1]


def memo_cost(p):
    """Top-down memoised variant used as a cross-check."""
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def go(i, j):
        if i == j:
            return 0
        return min(go(i, k) + go(k + 1, j) + p[i] * p[k + 1] * p[j + 1]
                   for k in range(i, j))

    return go(0, len(p) - 2)


if __name__ == "__main__":
    dims = [30, 35, 15, 5, 10, 20, 25]
    cost, split = matrix_chain_order(dims)
    assert cost[0][5] == 15125
    assert parenthesize(split, 0, 5) == "((A1(A2A3))((A4A5)A6))"
    assert min_multiplications([10, 20, 30]) == 6000
    assert min_multiplications([10, 20]) == 0
    assert min_multiplications([40, 20, 30, 10, 30]) == 26000
    for d in ([1, 2, 3, 4, 3], [5, 10, 3, 12, 5, 50, 6]):
        assert min_multiplications(d) == memo_cost(d)
    print("algo_39 matrix chain: all tests passed")

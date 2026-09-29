"""0/1 knapsack.

Given items with weights and values and a capacity, choose a subset
maximising total value without exceeding capacity; each item may be used
at most once. Full 2-D DP (with item reconstruction) and a 1-D rolling
array that iterates capacity downwards.
Time: O(nW). Space: O(nW) / O(W).
"""


def knapsack(weights, values, capacity):
    """Return (best_value, chosen_indices)."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]
            if w <= c and dp[i - 1][c - w] + v > dp[i][c]:
                dp[i][c] = dp[i - 1][c - w] + v
    chosen, c = [], capacity
    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen.append(i - 1)
            c -= weights[i - 1]
    return dp[n][capacity], sorted(chosen)


def knapsack_1d(weights, values, capacity):
    """Space-optimised value-only version."""
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def brute_force(weights, values, capacity):
    best = 0
    n = len(weights)
    for mask in range(1 << n):
        w = sum(weights[i] for i in range(n) if mask >> i & 1)
        if w <= capacity:
            best = max(best, sum(values[i] for i in range(n) if mask >> i & 1))
    return best


if __name__ == "__main__":
    W = [1, 3, 4, 5]
    V = [1, 4, 5, 7]
    best, items = knapsack(W, V, 7)
    assert best == 9
    assert sum(W[i] for i in items) <= 7 and sum(V[i] for i in items) == 9
    assert knapsack_1d(W, V, 7) == 9
    assert knapsack([10, 20, 30], [60, 100, 120], 50)[0] == 220
    assert knapsack([5], [10], 4) == (0, [])
    w2, v2 = [2, 3, 5, 7, 1, 4], [3, 4, 8, 9, 2, 5]
    for cap in range(0, 20):
        assert knapsack_1d(w2, v2, cap) == brute_force(w2, v2, cap)
    print("algo_37 0/1 knapsack: all tests passed")

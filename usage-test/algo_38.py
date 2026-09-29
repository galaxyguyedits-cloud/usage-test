"""Coin change problems.

(1) Minimum number of coins summing to an amount (unbounded supply),
with reconstruction of the coins used.
(2) Number of distinct combinations (order-insensitive) that make the
amount.
Also a greedy method that is only optimal for canonical coin systems.
Time: O(amount * len(coins)). Space: O(amount).
"""


def min_coins(coins, amount):
    """Return list of coins using the fewest coins, or None if impossible."""
    INF = float("inf")
    dp = [0] + [INF] * amount
    last = [None] * (amount + 1)
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                last[a] = c
    if dp[amount] == INF:
        return None
    out = []
    while amount:
        out.append(last[amount])
        amount -= last[amount]
    return sorted(out, reverse=True)


def count_ways(coins, amount):
    """Number of multisets of coins summing to amount."""
    ways = [1] + [0] * amount
    for c in coins:           # coin-outer loop avoids counting permutations
        for a in range(c, amount + 1):
            ways[a] += ways[a - c]
    return ways[amount]


def greedy_change(coins, amount):
    """Greedy: take the largest coin repeatedly. May be suboptimal."""
    out = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            out.append(c)
            amount -= c
    return out if amount == 0 else None


if __name__ == "__main__":
    assert min_coins([1, 2, 5], 11) == [5, 5, 1]
    assert min_coins([2], 3) is None
    assert min_coins([1], 0) == []
    # Greedy fails for non-canonical systems; DP succeeds.
    assert greedy_change([1, 3, 4], 6) == [4, 1, 1]
    assert min_coins([1, 3, 4], 6) == [3, 3]
    assert greedy_change([25, 10, 5, 1], 63) == [25, 25, 10, 1, 1, 1]
    assert count_ways([1, 2, 5], 5) == 4
    assert count_ways([2], 3) == 0
    assert count_ways([1, 5, 10, 25, 50], 100) == 292
    print("algo_38 coin change: all tests passed")

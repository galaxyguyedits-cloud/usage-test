"""Rod cutting.

Given a rod of length n and price[i] for a piece of length i+1, find the
maximum revenue obtainable by cutting the rod into pieces. Bottom-up DP
with reconstruction of the cut lengths, plus a variant charging a fixed
cost per cut.
Time: O(n^2). Space: O(n).
"""


def rod_cutting(prices, n):
    """Return (max_revenue, list_of_piece_lengths)."""
    revenue = [0] * (n + 1)
    first_cut = [0] * (n + 1)
    for length in range(1, n + 1):
        best = float("-inf")
        for cut in range(1, min(length, len(prices)) + 1):
            candidate = prices[cut - 1] + revenue[length - cut]
            if candidate > best:
                best = candidate
                first_cut[length] = cut
        revenue[length] = best if best != float("-inf") else 0
    pieces, rem = [], n
    while rem > 0 and first_cut[rem]:
        pieces.append(first_cut[rem])
        rem -= first_cut[rem]
    return revenue[n], pieces


def rod_cutting_with_cost(prices, n, cut_cost):
    """Max revenue when each cut costs cut_cost."""
    revenue = [0] * (n + 1)
    for length in range(1, n + 1):
        best = prices[length - 1] if length <= len(prices) else 0
        for cut in range(1, min(length - 1, len(prices)) + 1):
            best = max(best, prices[cut - 1] + revenue[length - cut] - cut_cost)
        revenue[length] = best
    return revenue[n]


def brute(prices, n):
    if n == 0:
        return 0
    return max(prices[i - 1] + brute(prices, n - i)
               for i in range(1, min(n, len(prices)) + 1))


if __name__ == "__main__":
    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    rev, pieces = rod_cutting(prices, 8)
    assert rev == 22
    assert sum(pieces) == 8
    assert sum(prices[p - 1] for p in pieces) == 22
    assert rod_cutting(prices, 4)[0] == 10
    assert rod_cutting(prices, 0) == (0, [])
    for n in range(1, 9):
        assert rod_cutting(prices, n)[0] == brute(prices, n)
    assert rod_cutting_with_cost(prices, 4, 0) == 10
    assert rod_cutting_with_cost(prices, 4, 2) == 9
    print("algo_40 rod cutting: all tests passed")

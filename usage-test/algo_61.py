"""Kadane's algorithm for maximum subarray sum.

Scans the array keeping the best sum of a subarray ending at the current
position (either extend the previous run or start fresh) and the best
seen overall. Tracks indices to return the subarray itself. Extensions:
maximum circular subarray and maximum-sum rectangle in a 2-D matrix.
Time: O(n) (O(r^2 c) for 2-D). Space: O(1).
"""


def max_subarray(arr):
    """Return (best_sum, start, end_exclusive) for non-empty arr."""
    best = cur = arr[0]
    best_lo, best_hi, lo = 0, 1, 0
    for i in range(1, len(arr)):
        if cur < 0:
            cur, lo = arr[i], i
        else:
            cur += arr[i]
        if cur > best:
            best, best_lo, best_hi = cur, lo, i + 1
    return best, best_lo, best_hi


def max_circular_subarray(arr):
    """Maximum subarray sum where the array wraps around."""
    straight = max_subarray(arr)[0]
    if straight < 0:
        return straight  # all negative
    total = sum(arr)
    min_sub = -max_subarray([-x for x in arr])[0]
    return max(straight, total - min_sub)


def max_rectangle(matrix):
    """Maximum sum of any sub-rectangle of a 2-D matrix."""
    rows, cols = len(matrix), len(matrix[0])
    best = float("-inf")
    for top in range(rows):
        col_sums = [0] * cols
        for bottom in range(top, rows):
            for c in range(cols):
                col_sums[c] += matrix[bottom][c]
            best = max(best, max_subarray(col_sums)[0])
    return best


def brute(arr):
    return max(sum(arr[i:j]) for i in range(len(arr)) for j in range(i + 1, len(arr) + 1))


if __name__ == "__main__":
    data = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    s, lo, hi = max_subarray(data)
    assert s == 6 and data[lo:hi] == [4, -1, 2, 1]
    assert max_subarray([-3, -1, -2])[0] == -1
    assert max_subarray([5])[0] == 5
    for arr in ([1, 2, 3], [2, -1, 2, -1, 2], [-1, 3, -2, 5, -7, 4]):
        assert max_subarray(arr)[0] == brute(arr)
    assert max_circular_subarray([5, -3, 5]) == 10
    assert max_circular_subarray([-3, -2, -3]) == -2
    assert max_circular_subarray([1, -2, 3, -2]) == 3
    m = [[1, 2, -1, -4, -20], [-8, -3, 4, 2, 1], [3, 8, 10, 1, 3], [-4, -1, 1, 7, -6]]
    assert max_rectangle(m) == 29
    print("algo_61 Kadane: all tests passed")

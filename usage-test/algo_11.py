"""Binary search.

Searches a sorted sequence by repeatedly halving the search interval.
Includes exact-match search plus lower_bound / upper_bound variants
(equivalent to bisect_left / bisect_right).
Time: O(log n). Space: O(1).
"""


def binary_search(arr, target):
    """Return an index of target in sorted arr, or -1 if absent."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def lower_bound(arr, target):
    """First index i such that arr[i] >= target (len(arr) if none)."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(arr, target):
    """First index i such that arr[i] > target (len(arr) if none)."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def count_occurrences(arr, target):
    """Number of times target appears in sorted arr."""
    return upper_bound(arr, target) - lower_bound(arr, target)


if __name__ == "__main__":
    import bisect

    data = [1, 3, 3, 3, 5, 8, 13, 21]
    assert binary_search(data, 8) == 5
    assert binary_search(data, 4) == -1
    assert binary_search([], 1) == -1
    assert data[binary_search(data, 3)] == 3
    for t in range(0, 25):
        assert lower_bound(data, t) == bisect.bisect_left(data, t)
        assert upper_bound(data, t) == bisect.bisect_right(data, t)
    assert count_occurrences(data, 3) == 3
    assert count_occurrences(data, 2) == 0
    print("algo_11 binary search: all tests passed")

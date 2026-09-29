"""Exponential search.

Finds the range in which the target may lie by doubling an index bound
(1, 2, 4, 8, ...) until it passes the target, then performs a binary
search within that range. Useful for unbounded or very large lists
where the target is near the beginning.
Time: O(log i) where i is the target's position. Space: O(1).
"""


def _binary_search(arr, target, lo, hi):
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def exponential_search(arr, target):
    """Return index of target in sorted arr, or -1."""
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0
    bound = 1
    while bound < n and arr[bound] < target:
        bound *= 2
    return _binary_search(arr, target, bound // 2, min(bound, n - 1))


def unbounded_search(get, target):
    """Search a conceptually infinite sorted sequence given by get(i).

    get(i) must be non-decreasing in i. Returns the index or -1.
    """
    if get(0) == target:
        return 0
    bound = 1
    while get(bound) < target:
        bound *= 2
    lo, hi = bound // 2, bound
    while lo <= hi:
        mid = (lo + hi) // 2
        v = get(mid)
        if v == target:
            return mid
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


if __name__ == "__main__":
    data = [2, 3, 4, 10, 40, 55, 70, 88, 91, 100]
    for i, v in enumerate(data):
        assert exponential_search(data, v) == i
    assert exponential_search(data, 41) == -1
    assert exponential_search(data, 1000) == -1
    assert exponential_search([], 5) == -1
    assert unbounded_search(lambda i: i * i, 144) == 12
    assert unbounded_search(lambda i: 3 * i, 10) == -1
    print("algo_13 exponential search: all tests passed")

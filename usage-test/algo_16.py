"""Quickselect.

Finds the k-th smallest element of an unsorted list without fully
sorting it, using quicksort-style partitioning but recursing only into
the side that contains the answer. Uses a deterministic pivot
(middle element) with three-way partitioning to handle duplicates.
Time: O(n) average, O(n^2) worst. Space: O(1) extra (iterative).
"""


def quickselect(items, k):
    """Return the k-th smallest element (0-indexed) of items."""
    if not 0 <= k < len(items):
        raise IndexError("k out of range")
    arr = list(items)
    lo, hi = 0, len(arr) - 1
    while True:
        if lo == hi:
            return arr[lo]
        pivot = arr[(lo + hi) // 2]
        # Dutch national flag partition of arr[lo..hi].
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[gt], arr[i] = arr[i], arr[gt]
                gt -= 1
            else:
                i += 1
        if k < lt:
            hi = lt - 1
        elif k > gt:
            lo = gt + 1
        else:
            return pivot


def median(items):
    """Return the median (average of middle two for even length)."""
    n = len(items)
    if n % 2:
        return quickselect(items, n // 2)
    return (quickselect(items, n // 2 - 1) + quickselect(items, n // 2)) / 2


def top_k(items, k):
    """Return the k largest items in descending order."""
    threshold = quickselect(items, len(items) - k)
    bigger = sorted((x for x in items if x > threshold), reverse=True)
    return (bigger + [threshold] * k)[:k]


if __name__ == "__main__":
    data = [7, 10, 4, 3, 20, 15, 4, 4]
    s = sorted(data)
    for k in range(len(data)):
        assert quickselect(data, k) == s[k]
    assert median([3, 1, 2]) == 2
    assert median([4, 1, 3, 2]) == 2.5
    assert top_k(data, 3) == [20, 15, 10]
    try:
        quickselect([1, 2], 5)
        assert False
    except IndexError:
        pass
    print("algo_16 quickselect: all tests passed")

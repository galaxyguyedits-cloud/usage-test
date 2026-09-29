"""Quick sort.

Picks a pivot, partitions the array so smaller elements come before it
and larger after, then recursively sorts the partitions. This version
uses in-place Lomuto partitioning with median-of-three pivot selection.
Time: O(n log n) average, O(n^2) worst. Space: O(log n) stack.
"""


def _median_of_three(arr, lo, hi):
    mid = (lo + hi) // 2
    if arr[mid] < arr[lo]:
        arr[mid], arr[lo] = arr[lo], arr[mid]
    if arr[hi] < arr[lo]:
        arr[hi], arr[lo] = arr[lo], arr[hi]
    if arr[mid] < arr[hi]:
        arr[mid], arr[hi] = arr[hi], arr[mid]
    # Now arr[hi] holds the median, used as the pivot.


def partition(arr, lo, hi):
    """Lomuto partition around arr[hi]; return final pivot index."""
    _median_of_three(arr, lo, hi)
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i


def quick_sort(items):
    """Return a new list sorted with in-place quick sort."""
    arr = list(items)
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        if lo < hi:
            p = partition(arr, lo, hi)
            stack.append((lo, p - 1))
            stack.append((p + 1, hi))
    return arr


def quick_sort_functional(items):
    """Simple (non in-place) three-way quick sort."""
    if len(items) <= 1:
        return list(items)
    pivot = items[len(items) // 2]
    less = [x for x in items if x < pivot]
    equal = [x for x in items if x == pivot]
    greater = [x for x in items if x > pivot]
    return quick_sort_functional(less) + equal + quick_sort_functional(greater)


if __name__ == "__main__":
    assert quick_sort([]) == []
    assert quick_sort([10, 7, 8, 9, 1, 5]) == [1, 5, 7, 8, 9, 10]
    assert quick_sort([4, 4, 4, 1]) == [1, 4, 4, 4]
    data = [3, -1, 99, 0, 3, 42, -7, 15, 8, 8]
    assert quick_sort(data) == sorted(data)
    assert quick_sort_functional(data) == sorted(data)
    assert quick_sort(list(range(50, 0, -1))) == list(range(1, 51))
    print("algo_05 quick sort: all tests passed")

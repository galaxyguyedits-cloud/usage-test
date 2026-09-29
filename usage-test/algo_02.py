"""Insertion sort.

Builds the sorted list one element at a time by inserting each new
element into its correct position among the already-sorted prefix.
Time: O(n^2) worst case, O(n) on nearly sorted data. Space: O(1).
Stable: equal elements keep their relative order.
"""


def insertion_sort(items, key=lambda x: x):
    """Return a new list sorted ascending by key using insertion sort."""
    arr = list(items)
    for i in range(1, len(arr)):
        current = arr[i]
        k = key(current)
        j = i - 1
        # Shift larger elements one slot to the right.
        while j >= 0 and key(arr[j]) > k:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr


def binary_insertion_sort(items):
    """Insertion sort variant that uses binary search to find the slot."""
    arr = []
    for x in items:
        lo, hi = 0, len(arr)
        while lo < hi:
            mid = (lo + hi) // 2
            if arr[mid] <= x:
                lo = mid + 1
            else:
                hi = mid
        arr.insert(lo, x)
    return arr


if __name__ == "__main__":
    assert insertion_sort([]) == []
    assert insertion_sort([4, 3, 2, 1]) == [1, 2, 3, 4]
    assert insertion_sort([1, 2, 3]) == [1, 2, 3]
    assert insertion_sort([2, -5, 0, 2, 9]) == [-5, 0, 2, 2, 9]
    # Stability check: sort by first element only.
    pairs = [(2, "a"), (1, "b"), (2, "c"), (1, "d")]
    assert insertion_sort(pairs, key=lambda p: p[0]) == [
        (1, "b"), (1, "d"), (2, "a"), (2, "c")
    ]
    data = [7, 3, 9, 1, 3, 0, 12]
    assert binary_insertion_sort(data) == sorted(data)
    assert insertion_sort(data) == sorted(data)
    print("algo_02 insertion sort: all tests passed")

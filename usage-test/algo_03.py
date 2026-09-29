"""Selection sort.

Repeatedly finds the minimum element in the unsorted suffix and swaps it
into the next position of the sorted prefix. Performs at most n-1 swaps,
which is useful when writes are expensive.
Time: O(n^2) in all cases. Space: O(1). Not stable.
"""


def selection_sort(items):
    """Return a new ascending list using selection sort."""
    arr = list(items)
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def selection_sort_swaps(items):
    """Return the number of swaps selection sort performs."""
    arr = list(items)
    swaps = 0
    for i in range(len(arr) - 1):
        min_idx = min(range(i, len(arr)), key=arr.__getitem__)
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
    return swaps


def double_selection_sort(items):
    """Select both min and max each pass, shrinking the range from both ends."""
    arr = list(items)
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mn = min(range(lo, hi + 1), key=arr.__getitem__)
        arr[lo], arr[mn] = arr[mn], arr[lo]
        mx = max(range(lo, hi + 1), key=arr.__getitem__)
        arr[hi], arr[mx] = arr[mx], arr[hi]
        lo += 1
        hi -= 1
    return arr


if __name__ == "__main__":
    assert selection_sort([]) == []
    assert selection_sort([64, 25, 12, 22, 11]) == [11, 12, 22, 25, 64]
    assert selection_sort([1, 1, 1]) == [1, 1, 1]
    assert selection_sort([-3, 10, -3, 0]) == [-3, -3, 0, 10]
    assert selection_sort_swaps([1, 2, 3]) == 0
    assert selection_sort_swaps([3, 2, 1]) == 1
    sample = [5, 9, 1, 7, 3, 3, 8, 0]
    assert double_selection_sort(sample) == sorted(sample)
    print("algo_03 selection sort: all tests passed")

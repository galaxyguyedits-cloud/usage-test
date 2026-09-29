"""Bubble sort.

Repeatedly steps through the list, compares adjacent elements and swaps
them if they are in the wrong order. Stops early when a full pass makes
no swaps. Time: O(n^2) worst case, O(n) best case. Space: O(1).
"""


def bubble_sort(items):
    """Return a new list containing items sorted in ascending order."""
    arr = list(items)
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        # After each pass, the largest remaining element is in place.
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def is_sorted(arr):
    """Return True if arr is in non-decreasing order."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def count_passes(items):
    """Return how many passes bubble sort needs for the given input."""
    arr = list(items)
    n = len(arr)
    passes = 0
    for i in range(n - 1):
        passes += 1
        swapped = False
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return passes


if __name__ == "__main__":
    assert bubble_sort([]) == []
    assert bubble_sort([1]) == [1]
    assert bubble_sort([5, 1, 4, 2, 8]) == [1, 2, 4, 5, 8]
    assert bubble_sort([3, 3, 1, 2]) == [1, 2, 3, 3]
    assert bubble_sort(["b", "a", "c"]) == ["a", "b", "c"]
    assert is_sorted(bubble_sort([9, -1, 0, 7, 7, 2]))
    assert count_passes([1, 2, 3, 4]) == 1
    print("algo_01 bubble sort: all tests passed")

"""Heap sort.

Builds a max-heap in place, then repeatedly swaps the root (maximum) to
the end of the array and restores the heap property on the shrunk heap.
Time: O(n log n) in all cases. Space: O(1). Not stable.
"""


def sift_down(arr, start, end):
    """Restore max-heap property for the subtree rooted at start.

    Only indices < end are considered part of the heap.
    """
    root = start
    while True:
        child = 2 * root + 1
        if child >= end:
            return
        if child + 1 < end and arr[child + 1] > arr[child]:
            child += 1
        if arr[root] < arr[child]:
            arr[root], arr[child] = arr[child], arr[root]
            root = child
        else:
            return


def heapify(arr):
    """Rearrange arr into a max-heap in place."""
    for start in range(len(arr) // 2 - 1, -1, -1):
        sift_down(arr, start, len(arr))


def is_max_heap(arr):
    """Return True if arr satisfies the max-heap property."""
    n = len(arr)
    return all(arr[(i - 1) // 2] >= arr[i] for i in range(1, n))


def heap_sort(items):
    """Return a new ascending list sorted using heap sort."""
    arr = list(items)
    heapify(arr)
    for end in range(len(arr) - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        sift_down(arr, 0, end)
    return arr


if __name__ == "__main__":
    h = [3, 1, 6, 5, 2, 4]
    heapify(h)
    assert is_max_heap(h)
    assert h[0] == 6
    assert heap_sort([]) == []
    assert heap_sort([12, 11, 13, 5, 6, 7]) == [5, 6, 7, 11, 12, 13]
    assert heap_sort([2, 2, 1]) == [1, 2, 2]
    data = [9, -4, 0, 17, 3, 3, 21, -8]
    assert heap_sort(data) == sorted(data)
    print("algo_06 heap sort: all tests passed")

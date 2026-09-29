"""Merge sort.

Divide-and-conquer: split the list in half, recursively sort each half,
then merge the two sorted halves. Also includes inversion counting,
which piggybacks on the merge step.
Time: O(n log n). Space: O(n). Stable.
"""


def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(items):
    """Return a new sorted list using top-down merge sort."""
    if len(items) <= 1:
        return list(items)
    mid = len(items) // 2
    return merge(merge_sort(items[:mid]), merge_sort(items[mid:]))


def count_inversions(items):
    """Return (sorted_list, number of pairs i<j with items[i] > items[j])."""
    if len(items) <= 1:
        return list(items), 0
    mid = len(items) // 2
    left, a = count_inversions(items[:mid])
    right, b = count_inversions(items[mid:])
    merged, i, j, inv = [], 0, 0, a + b
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            inv += len(left) - i
            j += 1
    merged += left[i:] + right[j:]
    return merged, inv


if __name__ == "__main__":
    assert merge([1, 4], [2, 3]) == [1, 2, 3, 4]
    assert merge_sort([]) == []
    assert merge_sort([38, 27, 43, 3, 9, 82, 10]) == [3, 9, 10, 27, 38, 43, 82]
    assert merge_sort([2, 1, 2, 1]) == [1, 1, 2, 2]
    assert count_inversions([1, 2, 3])[1] == 0
    assert count_inversions([3, 2, 1])[1] == 3
    assert count_inversions([2, 4, 1, 3, 5]) == ([1, 2, 3, 4, 5], 3)
    print("algo_04 merge sort: all tests passed")

"""Dutch national flag partitioning (Dijkstra's 3-way partition).

Rearranges an array of three kinds of values (e.g. 0, 1, 2) in a single
pass using three pointers: everything before `low` is 0, between `low`
and `mid` is 1, after `high` is 2, and [mid, high] is unprocessed.
Generalised to partition around any pivot, and used to sort colours.
Time: O(n). Space: O(1).
"""


def sort_colors(nums):
    """Sort a list of 0s, 1s and 2s in place; return it."""
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
    return nums


def three_way_partition(nums, pivot):
    """Partition in place into < pivot, == pivot, > pivot.

    Returns (lt, gt): nums[:lt] < pivot, nums[lt:gt] == pivot,
    nums[gt:] > pivot.
    """
    lt, i, gt = 0, 0, len(nums)
    while i < gt:
        if nums[i] < pivot:
            nums[lt], nums[i] = nums[i], nums[lt]
            lt += 1
            i += 1
        elif nums[i] > pivot:
            gt -= 1
            nums[i], nums[gt] = nums[gt], nums[i]
        else:
            i += 1
    return lt, gt


def segregate(items, key):
    """Stable-free grouping of items into three classes by key -> 0/1/2."""
    keyed = [(key(x), x) for x in items]
    lo, mid, hi = 0, 0, len(keyed) - 1
    while mid <= hi:
        k = keyed[mid][0]
        if k == 0:
            keyed[lo], keyed[mid] = keyed[mid], keyed[lo]
            lo += 1
            mid += 1
        elif k == 1:
            mid += 1
        else:
            keyed[mid], keyed[hi] = keyed[hi], keyed[mid]
            hi -= 1
    return [x for _, x in keyed]


if __name__ == "__main__":
    assert sort_colors([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]
    assert sort_colors([]) == [] and sort_colors([1]) == [1]
    assert sort_colors([2, 2, 0]) == [0, 2, 2]
    arr = [9, 3, 5, 3, 1, 7, 3, 8, 0]
    lt, gt = three_way_partition(arr, 3)
    assert all(x < 3 for x in arr[:lt])
    assert all(x == 3 for x in arr[lt:gt]) and gt - lt == 3
    assert all(x > 3 for x in arr[gt:])
    nums = [5, -2, 0, 8, -7, 0, 3]
    out = segregate(nums, lambda x: 0 if x < 0 else (1 if x == 0 else 2))
    assert sorted(out[:2]) == [-7, -2] and out[2:4] == [0, 0]
    assert sorted(out[4:]) == [3, 5, 8]
    print("algo_72 Dutch national flag: all tests passed")

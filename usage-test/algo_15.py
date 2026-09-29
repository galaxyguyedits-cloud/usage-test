"""Jump search.

Searches a sorted array by jumping ahead in fixed blocks of size
sqrt(n) until the block containing the target is found, then performs a
linear scan inside that block.
Time: O(sqrt(n)). Space: O(1).
"""

import math


def jump_search(arr, target):
    """Return index of target in sorted arr, or -1."""
    n = len(arr)
    if n == 0:
        return -1
    step = int(math.isqrt(n)) or 1
    prev, curr = 0, step
    # Jump until the end of the current block is >= target.
    while curr < n and arr[curr - 1] < target:
        prev = curr
        curr += step
    # Linear scan within the block [prev, min(curr, n)).
    for i in range(prev, min(curr, n)):
        if arr[i] == target:
            return i
        if arr[i] > target:
            break
    return -1


def jump_search_steps(arr, target):
    """Return (index, comparisons) to illustrate the cost."""
    n = len(arr)
    step = int(math.isqrt(n)) or 1
    prev, curr, comps = 0, step, 0
    while curr < n and arr[curr - 1] < target:
        comps += 1
        prev = curr
        curr += step
    for i in range(prev, min(curr, n)):
        comps += 1
        if arr[i] == target:
            return i, comps
    return -1, comps


if __name__ == "__main__":
    data = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    assert jump_search(data, 55) == 10
    assert jump_search(data, 0) == 0
    assert jump_search(data, 610) == 15
    assert jump_search(data, 4) == -1
    assert jump_search(data, 1000) == -1
    assert jump_search([], 3) == -1
    big = list(range(0, 10000, 3))
    idx, comps = jump_search_steps(big, 2997)
    assert idx == 999 and comps <= 2 * math.isqrt(len(big)) + 2
    print("algo_15 jump search: all tests passed")

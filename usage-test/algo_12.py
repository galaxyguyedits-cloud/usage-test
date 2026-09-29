"""Interpolation search.

Improves on binary search for uniformly distributed sorted data by
estimating the probe position from the target's value relative to the
current bounds, like looking up a word in a dictionary.
Time: O(log log n) average on uniform data, O(n) worst. Space: O(1).
"""


def interpolation_search(arr, target):
    """Return index of target in sorted numeric arr, or -1."""
    lo, hi = 0, len(arr) - 1
    probes = 0
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        probes += 1
        if arr[hi] == arr[lo]:
            return lo if arr[lo] == target else -1
        # Estimate position proportionally.
        pos = lo + (target - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo])
        if arr[pos] == target:
            return pos
        if arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1


def interpolation_probes(arr, target):
    """Return the number of probes made while searching for target."""
    lo, hi, probes = 0, len(arr) - 1, 0
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        probes += 1
        if arr[hi] == arr[lo]:
            break
        pos = lo + (target - arr[lo]) * (hi - lo) // (arr[hi] - arr[lo])
        if arr[pos] == target:
            break
        if arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return probes


if __name__ == "__main__":
    uniform = list(range(0, 1000, 5))
    assert interpolation_search(uniform, 500) == 100
    assert interpolation_search(uniform, 0) == 0
    assert interpolation_search(uniform, 995) == 199
    assert interpolation_search(uniform, 502) == -1
    assert interpolation_search([], 3) == -1
    assert interpolation_search([7, 7, 7], 7) == 0
    skewed = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    for i, v in enumerate(skewed):
        assert interpolation_search(skewed, v) == i
    assert interpolation_probes(uniform, 735) == 1
    print("algo_12 interpolation search: all tests passed")

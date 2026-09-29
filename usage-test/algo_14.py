"""Ternary search.

Two uses: (1) searching a sorted array by splitting it into three parts,
and (2) finding the extremum of a unimodal function on an interval by
discarding one third of the interval each iteration.
Time: O(log n) / O(log((hi-lo)/eps)). Space: O(1).
"""


def ternary_search_array(arr, target):
    """Return index of target in sorted arr, or -1."""
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        third = (hi - lo) // 3
        m1, m2 = lo + third, hi - third
        if arr[m1] == target:
            return m1
        if arr[m2] == target:
            return m2
        if target < arr[m1]:
            hi = m1 - 1
        elif target > arr[m2]:
            lo = m2 + 1
        else:
            lo, hi = m1 + 1, m2 - 1
    return -1


def ternary_max(f, lo, hi, eps=1e-9):
    """Return x in [lo, hi] maximising unimodal function f."""
    while hi - lo > eps:
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            lo = m1
        else:
            hi = m2
    return (lo + hi) / 2


def ternary_min(f, lo, hi, eps=1e-9):
    """Return x in [lo, hi] minimising unimodal function f."""
    return ternary_max(lambda x: -f(x), lo, hi, eps)


if __name__ == "__main__":
    data = [1, 4, 9, 16, 25, 36, 49, 64, 81]
    for i, v in enumerate(data):
        assert ternary_search_array(data, v) == i
    assert ternary_search_array(data, 50) == -1
    assert ternary_search_array([], 1) == -1
    x = ternary_max(lambda t: -(t - 2.5) ** 2 + 7, -10, 10)
    assert abs(x - 2.5) < 1e-6
    y = ternary_min(lambda t: (t + 1) ** 2, -5, 5)
    assert abs(y + 1) < 1e-6
    print("algo_14 ternary search: all tests passed")

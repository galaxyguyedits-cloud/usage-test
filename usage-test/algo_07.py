"""Counting sort.

Non-comparison sort for integers within a known range. Counts the
occurrences of each value, computes prefix sums to find final positions,
then places elements (iterating backwards to stay stable).
Time: O(n + k) where k is the value range. Space: O(n + k).
"""


def counting_sort(items, key=lambda x: x):
    """Stable counting sort of items by integer key (may be negative)."""
    items = list(items)
    if not items:
        return []
    keys = [key(x) for x in items]
    lo, hi = min(keys), max(keys)
    counts = [0] * (hi - lo + 1)
    for k in keys:
        counts[k - lo] += 1
    # Prefix sums: counts[i] becomes the end position of value lo+i.
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    output = [None] * len(items)
    for x, k in zip(reversed(items), reversed(keys)):
        counts[k - lo] -= 1
        output[counts[k - lo]] = x
    return output


def histogram(items):
    """Return a dict mapping each value to how often it occurs."""
    result = {}
    for x in items:
        result[x] = result.get(x, 0) + 1
    return result


def simple_counting_sort(items):
    """Non-stable version that rebuilds output directly from counts."""
    if not items:
        return []
    lo, hi = min(items), max(items)
    counts = [0] * (hi - lo + 1)
    for x in items:
        counts[x - lo] += 1
    out = []
    for offset, c in enumerate(counts):
        out.extend([offset + lo] * c)
    return out


if __name__ == "__main__":
    assert counting_sort([]) == []
    assert counting_sort([4, 2, 2, 8, 3, 3, 1]) == [1, 2, 2, 3, 3, 4, 8]
    assert counting_sort([-5, 0, -2, 3, -5]) == [-5, -5, -2, 0, 3]
    recs = [(3, "x"), (1, "y"), (3, "z"), (0, "w")]
    assert counting_sort(recs, key=lambda r: r[0]) == [
        (0, "w"), (1, "y"), (3, "x"), (3, "z")
    ]
    assert simple_counting_sort([9, 1, 5, 1]) == [1, 1, 5, 9]
    assert histogram([1, 1, 2]) == {1: 2, 2: 1}
    print("algo_07 counting sort: all tests passed")

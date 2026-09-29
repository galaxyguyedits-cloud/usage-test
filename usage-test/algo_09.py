"""Shell sort.

Generalisation of insertion sort that first sorts elements far apart
(gap-sorted), then progressively reduces the gap. Uses Ciura's gap
sequence extended geometrically for large inputs.
Time: roughly O(n^1.3) in practice. Space: O(1).
"""

CIURA_GAPS = [1, 4, 10, 23, 57, 132, 301, 701]


def gap_sequence(n):
    """Return gaps (descending) suitable for an array of length n."""
    gaps = list(CIURA_GAPS)
    while gaps[-1] * 2.25 < n:
        gaps.append(int(gaps[-1] * 2.25))
    return [g for g in reversed(gaps) if g < n] or [1]


def shell_sort(items):
    """Return a new ascending list using shell sort."""
    arr = list(items)
    n = len(arr)
    for gap in gap_sequence(n):
        # Gapped insertion sort.
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
    return arr


def shell_sort_halving(items):
    """Shell sort with Shell's original n/2, n/4, ... gap sequence."""
    arr = list(items)
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp, j = arr[i], i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


if __name__ == "__main__":
    assert gap_sequence(5) == [4, 1]
    assert shell_sort([]) == []
    assert shell_sort([12, 34, 54, 2, 3]) == [2, 3, 12, 34, 54]
    big = [(i * 7919) % 1009 for i in range(1500)]
    assert shell_sort(big) == sorted(big)
    assert shell_sort_halving(big) == sorted(big)
    assert shell_sort([5, -1, 5, 0]) == [-1, 0, 5, 5]
    print("algo_09 shell sort: all tests passed")

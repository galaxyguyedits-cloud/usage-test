"""Radix sort (LSD).

Sorts non-negative integers digit by digit, starting from the least
significant digit, using a stable bucket pass for each digit. Negative
numbers are handled by sorting them separately by absolute value.
Time: O(d * (n + b)) for d digits in base b. Space: O(n + b).
"""


def _radix_pass(arr, exp, base):
    buckets = [[] for _ in range(base)]
    for x in arr:
        buckets[(x // exp) % base].append(x)
    return [x for bucket in buckets for x in bucket]


def radix_sort_nonneg(items, base=10):
    """LSD radix sort for non-negative integers."""
    arr = list(items)
    if not arr:
        return arr
    largest = max(arr)
    exp = 1
    while largest // exp > 0:
        arr = _radix_pass(arr, exp, base)
        exp *= base
    return arr


def radix_sort(items, base=10):
    """Radix sort supporting negative integers."""
    negatives = [-x for x in items if x < 0]
    positives = [x for x in items if x >= 0]
    neg_sorted = [-x for x in reversed(radix_sort_nonneg(negatives, base))]
    return neg_sorted + radix_sort_nonneg(positives, base)


def num_digits(n, base=10):
    """Number of base-`base` digits in non-negative integer n."""
    if n == 0:
        return 1
    count = 0
    while n:
        n //= base
        count += 1
    return count


if __name__ == "__main__":
    assert radix_sort([]) == []
    assert radix_sort([170, 45, 75, 90, 802, 24, 2, 66]) == [
        2, 24, 45, 66, 75, 90, 170, 802
    ]
    assert radix_sort([-3, 15, -100, 0, 7, -3]) == [-100, -3, -3, 0, 7, 15]
    data = [1023, 5, 64, 512, 7, 7, 0, 999]
    assert radix_sort(data, base=2) == sorted(data)
    assert radix_sort(data, base=16) == sorted(data)
    assert num_digits(0) == 1 and num_digits(999) == 3 and num_digits(8, 2) == 4
    print("algo_08 radix sort: all tests passed")

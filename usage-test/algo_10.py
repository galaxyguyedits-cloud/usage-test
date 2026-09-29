"""Bucket sort.

Distributes elements into a number of buckets by value range, sorts each
bucket individually (here with insertion sort), and concatenates them.
Works best when input is uniformly distributed.
Time: O(n + k) average, O(n^2) worst. Space: O(n + k).
"""


def _insertion_sort(bucket):
    for i in range(1, len(bucket)):
        cur, j = bucket[i], i - 1
        while j >= 0 and bucket[j] > cur:
            bucket[j + 1] = bucket[j]
            j -= 1
        bucket[j + 1] = cur
    return bucket


def bucket_sort(items, num_buckets=None):
    """Sort numeric items using bucket sort."""
    arr = list(items)
    if len(arr) <= 1:
        return arr
    k = num_buckets or len(arr)
    lo, hi = min(arr), max(arr)
    if lo == hi:
        return arr
    width = (hi - lo) / k
    buckets = [[] for _ in range(k)]
    for x in arr:
        idx = int((x - lo) / width)
        if idx == k:  # the maximum element lands in the last bucket
            idx = k - 1
        buckets[idx].append(x)
    result = []
    for b in buckets:
        result.extend(_insertion_sort(b))
    return result


def bucket_sizes(items, num_buckets):
    """Return the size of each bucket (useful for inspecting balance)."""
    lo, hi = min(items), max(items)
    width = (hi - lo) / num_buckets or 1
    sizes = [0] * num_buckets
    for x in items:
        sizes[min(int((x - lo) / width), num_buckets - 1)] += 1
    return sizes


if __name__ == "__main__":
    assert bucket_sort([]) == []
    floats = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    assert bucket_sort(floats) == sorted(floats)
    ints = [29, 25, 3, 49, 9, 37, 21, 43]
    assert bucket_sort(ints, 5) == sorted(ints)
    assert bucket_sort([7, 7, 7]) == [7, 7, 7]
    assert bucket_sort([-2.5, 3.0, 0.0, -10.0]) == [-10.0, -2.5, 0.0, 3.0]
    assert sum(bucket_sizes(ints, 4)) == len(ints)
    print("algo_10 bucket sort: all tests passed")

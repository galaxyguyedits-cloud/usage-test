"""Permutations.

Generates permutations by backtracking (swap-based), computes the next
lexicographic permutation in place (Narayana Pandita's algorithm),
Heap's algorithm (each step differs by a single swap), and ranks a
permutation in lexicographic order via the factorial number system.
"""

from math import factorial


def permutations(items):
    """Return all permutations of items via backtracking."""
    arr = list(items)
    out = []

    def backtrack(k):
        if k == len(arr):
            out.append(list(arr))
            return
        for i in range(k, len(arr)):
            arr[k], arr[i] = arr[i], arr[k]
            backtrack(k + 1)
            arr[k], arr[i] = arr[i], arr[k]

    backtrack(0)
    return out


def next_permutation(arr):
    """Transform arr into its next lexicographic permutation.

    Returns False (and leaves arr sorted ascending) if arr was the last.
    """
    i = len(arr) - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    if i >= 0:
        j = len(arr) - 1
        while arr[j] <= arr[i]:
            j -= 1
        arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1:] = reversed(arr[i + 1:])
    return i >= 0


def heaps_algorithm(items):
    arr, out = list(items), []
    c = [0] * len(arr)
    out.append(list(arr))
    i = 0
    while i < len(arr):
        if c[i] < i:
            j = 0 if i % 2 == 0 else c[i]
            arr[j], arr[i] = arr[i], arr[j]
            out.append(list(arr))
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1
    return out


def perm_rank(perm):
    """0-based lexicographic rank of a permutation of distinct items."""
    rank, remaining = 0, sorted(perm)
    for i, x in enumerate(perm):
        idx = remaining.index(x)
        rank += idx * factorial(len(perm) - 1 - i)
        remaining.pop(idx)
    return rank


if __name__ == "__main__":
    ps = permutations([1, 2, 3])
    assert len(ps) == 6 and sorted(ps) == [
        [1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    arr, seq = [1, 2, 3], [[1, 2, 3]]
    while next_permutation(arr):
        seq.append(list(arr))
    assert seq == sorted(ps) and arr == [1, 2, 3]
    a = [1, 1, 2]
    assert next_permutation(a) and a == [1, 2, 1]
    h = heaps_algorithm("abcd")
    assert len(h) == 24 and len({tuple(p) for p in h}) == 24
    assert perm_rank([1, 2, 3]) == 0 and perm_rank([3, 2, 1]) == 5
    assert perm_rank([2, 1, 3]) == 2
    print("algo_59 permutations: all tests passed")

"""Rabin-Karp string matching.

Uses a rolling polynomial hash to compare the pattern's hash with the
hash of every window of the text in O(1) per shift, verifying actual
characters only on hash hits (to rule out collisions).
Time: O(n + m) expected, O(nm) worst. Space: O(1).
"""

BASE = 256
MOD = 1_000_000_007


def rabin_karp(text, pattern):
    """Return start indices of all occurrences of pattern in text."""
    n, m = len(text), len(pattern)
    if m == 0:
        return list(range(n + 1))
    if m > n:
        return []
    high = pow(BASE, m - 1, MOD)  # weight of the leading character
    p_hash = t_hash = 0
    for i in range(m):
        p_hash = (p_hash * BASE + ord(pattern[i])) % MOD
        t_hash = (t_hash * BASE + ord(text[i])) % MOD
    result = []
    for s in range(n - m + 1):
        if p_hash == t_hash and text[s:s + m] == pattern:
            result.append(s)
        if s < n - m:
            t_hash = (t_hash - ord(text[s]) * high) % MOD
            t_hash = (t_hash * BASE + ord(text[s + m])) % MOD
    return result


def multi_pattern(text, patterns):
    """Search several equal-length patterns in one pass using a hash set."""
    m = len(patterns[0])
    assert all(len(p) == m for p in patterns)
    wanted = set(patterns)
    found = {p: [] for p in patterns}
    for i in range(len(text) - m + 1):
        window = text[i:i + m]
        if window in wanted:
            found[window].append(i)
    return found


def longest_repeated_length(s):
    """Length of the longest substring occurring at least twice."""
    lo, hi = 0, len(s)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        seen = {s[i:i + mid] for i in range(len(s) - mid + 1)}
        if len(seen) < len(s) - mid + 1:
            lo = mid
        else:
            hi = mid - 1
    return lo


if __name__ == "__main__":
    assert rabin_karp("GEEKS FOR GEEKS", "GEEK") == [0, 10]
    assert rabin_karp("aaaa", "aa") == [0, 1, 2]
    assert rabin_karp("abc", "abcd") == []
    assert rabin_karp("abracadabra", "abra") == [0, 7]
    assert rabin_karp("xy", "") == [0, 1, 2]
    found = multi_pattern("banana bandana", ["ana", "ban"])
    assert found == {"ana": [1, 3, 11], "ban": [0, 7]}
    assert longest_repeated_length("banana") == 3
    assert longest_repeated_length("abc") == 0
    print("algo_30 Rabin-Karp: all tests passed")

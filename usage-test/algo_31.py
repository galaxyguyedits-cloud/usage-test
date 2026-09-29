"""Z-algorithm.

Computes the Z-array: Z[i] is the length of the longest substring
starting at i that is also a prefix of the string. Maintains a window
[l, r) of the rightmost prefix-match to reuse earlier work. Pattern
search is done on pattern + sentinel + text.
Time: O(n). Space: O(n).
"""


def z_array(s):
    """Return the Z-array of s (Z[0] is defined as len(s))."""
    n = len(s)
    z = [0] * n
    if n == 0:
        return z
    z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def z_search(text, pattern):
    """Return all start indices of pattern in text using the Z-array."""
    if not pattern:
        return list(range(len(text) + 1))
    combined = pattern + "\x00" + text
    z = z_array(combined)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] >= m]


def count_distinct_substrings(s):
    """Count distinct substrings using incremental Z-arrays. O(n^2)."""
    total = 0
    cur = ""
    for ch in s:
        cur += ch
        rev = cur[::-1]
        z = z_array(rev)
        max_z = max(z[1:], default=0)
        total += len(cur) - max_z
    return total


if __name__ == "__main__":
    assert z_array("aaaaa") == [5, 4, 3, 2, 1]
    assert z_array("aabxaab") == [7, 1, 0, 0, 3, 1, 0]
    assert z_array("") == []
    assert z_search("baabaa", "aab") == [1]
    assert z_search("abababab", "abab") == [0, 2, 4]
    assert z_search("xyz", "q") == []
    assert count_distinct_substrings("abc") == 6
    assert count_distinct_substrings("aaa") == 3
    assert count_distinct_substrings("abab") == 7
    print("algo_31 Z-algorithm: all tests passed")

"""Knuth-Morris-Pratt (KMP) string matching.

Precomputes the failure function (longest proper prefix of the pattern
that is also a suffix, for each prefix) so that on a mismatch the search
never re-examines text characters.
Time: O(n + m). Space: O(m).
"""


def prefix_function(pattern):
    """Return the KMP failure array for pattern."""
    pi = [0] * len(pattern)
    k = 0
    for i in range(1, len(pattern)):
        while k > 0 and pattern[i] != pattern[k]:
            k = pi[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        pi[i] = k
    return pi


def kmp_search(text, pattern):
    """Return the list of start indices where pattern occurs in text."""
    if not pattern:
        return list(range(len(text) + 1))
    pi = prefix_function(pattern)
    matches = []
    k = 0
    for i, ch in enumerate(text):
        while k > 0 and ch != pattern[k]:
            k = pi[k - 1]
        if ch == pattern[k]:
            k += 1
        if k == len(pattern):
            matches.append(i - k + 1)
            k = pi[k - 1]
    return matches


def smallest_period(s):
    """Length of the smallest string p such that s is a prefix of p*∞."""
    if not s:
        return 0
    return len(s) - prefix_function(s)[-1]


if __name__ == "__main__":
    assert prefix_function("ababaca") == [0, 0, 1, 2, 3, 0, 1]
    assert prefix_function("aabaaab") == [0, 1, 0, 1, 2, 2, 3]
    assert kmp_search("ababcabcabababd", "ababd") == [10]
    assert kmp_search("aaaaa", "aa") == [0, 1, 2, 3]
    assert kmp_search("hello", "xyz") == []
    assert kmp_search("abc", "") == [0, 1, 2, 3]
    text = "the cat sat on the mat with the hat"
    assert kmp_search(text, "the") == [0, 15, 28]
    assert smallest_period("abcabcab") == 3
    assert smallest_period("aaaa") == 1
    print("algo_29 KMP: all tests passed")

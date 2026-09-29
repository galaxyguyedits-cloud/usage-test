"""Manacher's algorithm for the longest palindromic substring.

Transforms the string by interleaving a separator ("#") so every
palindrome has odd length, then computes the palindrome radius at each
centre, reusing mirrored radii inside the current rightmost palindrome.
Time: O(n). Space: O(n).
"""


def manacher_radii(s):
    """Return radii array over the transformed string ^#a#b#...#$."""
    t = "^#" + "#".join(s) + "#$"
    p = [0] * len(t)
    center = right = 0
    for i in range(1, len(t) - 1):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > right:
            center, right = i, i + p[i]
    return p


def longest_palindrome(s):
    """Return the longest palindromic substring of s (leftmost on ties)."""
    if not s:
        return ""
    p = manacher_radii(s)
    best_len, best_center = max((v, -i) for i, v in enumerate(p))
    best_center = -best_center
    start = (best_center - best_len) // 2
    return s[start:start + best_len]


def count_palindromic_substrings(s):
    """Total number of palindromic substrings (counted by position)."""
    p = manacher_radii(s)
    return sum((v + 1) // 2 for v in p[1:-1])


def brute_longest(s):
    best = ""
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub = s[i:j + 1]
            if sub == sub[::-1] and len(sub) > len(best):
                best = sub
    return best


if __name__ == "__main__":
    assert longest_palindrome("babad") == "bab"
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("forgeeksskeegfor") == "geeksskeeg"
    assert longest_palindrome("a") == "a"
    assert longest_palindrome("") == ""
    for word in ["abacdfgdcaba", "racecar", "abcde", "aaaabaaa"]:
        assert len(longest_palindrome(word)) == len(brute_longest(word))
    assert count_palindromic_substrings("abc") == 3
    assert count_palindromic_substrings("aaa") == 6
    print("algo_32 Manacher: all tests passed")

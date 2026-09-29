"""Longest common subsequence (LCS).

Finds the longest sequence that appears (not necessarily contiguously)
in both inputs. DP table dp[i][j] = LCS length of a[:i] and b[:j];
backtracking recovers one optimal subsequence. Also includes the
related shortest common supersequence length.
Time: O(nm). Space: O(nm).
"""


def lcs_table(a, b):
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def lcs(a, b):
    """Return one longest common subsequence as a string (or list)."""
    dp = lcs_table(a, b)
    i, j = len(a), len(b)
    out = []
    while i and j:
        if a[i - 1] == b[j - 1]:
            out.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    out.reverse()
    return "".join(out) if isinstance(a, str) else out


def lcs_length(a, b):
    return lcs_table(a, b)[-1][-1]


def is_subsequence(sub, seq):
    it = iter(seq)
    return all(ch in it for ch in sub)


def scs_length(a, b):
    """Length of the shortest common supersequence."""
    return len(a) + len(b) - lcs_length(a, b)


if __name__ == "__main__":
    assert lcs_length("ABCBDAB", "BDCABA") == 4
    s = lcs("ABCBDAB", "BDCABA")
    assert len(s) == 4
    assert is_subsequence(s, "ABCBDAB") and is_subsequence(s, "BDCABA")
    assert lcs("AGGTAB", "GXTXAYB") == "GTAB"
    assert lcs("", "abc") == ""
    assert lcs([1, 2, 3, 4], [2, 4, 3]) in ([2, 3], [2, 4])
    assert scs_length("geek", "eke") == 5
    assert not is_subsequence("axc", "ahbgdc")
    print("algo_35 LCS: all tests passed")

"""Levenshtein edit distance.

Minimum number of single-character insertions, deletions and
substitutions to transform one string into another. Classic DP with a
full table (for backtracking operations) and a two-row space-optimised
version.
Time: O(nm). Space: O(nm) / O(min(n, m)).
"""


def edit_distance_table(a, b):
    """Return the full DP table; dp[i][j] = distance(a[:i], b[:j])."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,       # delete
                           dp[i][j - 1] + 1,       # insert
                           dp[i - 1][j - 1] + cost)  # substitute / match
    return dp


def edit_distance(a, b):
    """Space-optimised distance using two rows."""
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def edit_operations(a, b):
    """Return a list of operations transforming a into b."""
    dp = edit_distance_table(a, b)
    i, j, ops = len(a), len(b), []
    while i > 0 or j > 0:
        if i and j and a[i - 1] == b[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
            i, j = i - 1, j - 1
        elif i and j and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(("sub", a[i - 1], b[j - 1]))
            i, j = i - 1, j - 1
        elif i and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(("del", a[i - 1]))
            i -= 1
        else:
            ops.append(("ins", b[j - 1]))
            j -= 1
    return ops[::-1]


if __name__ == "__main__":
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("flaw", "lawn") == 2
    assert edit_distance("", "abc") == 3
    assert edit_distance("same", "same") == 0
    assert edit_distance_table("intention", "execution")[-1][-1] == 5
    ops = edit_operations("kitten", "sitting")
    assert len(ops) == 3
    assert ("ins", "g") in ops
    print("algo_34 edit distance: all tests passed")

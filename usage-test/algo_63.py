"""Sliding window algorithms.

- sliding window maximum using a monotonic deque of indices, O(n)
- longest substring without repeating characters, O(n)
- minimum window substring containing all characters of a pattern, O(n)
- smallest subarray with sum >= target (positive numbers), O(n)
"""

from collections import Counter, deque


def window_max(nums, k):
    """Maximum of every contiguous window of size k."""
    dq, out = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def longest_unique_substring(s):
    last, start, best = {}, 0, 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best


def min_window(s, t):
    """Smallest substring of s containing every char of t (with counts)."""
    need = Counter(t)
    missing = len(t)
    lo = best_lo = 0
    best_len = float("inf")
    for hi, ch in enumerate(s, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while need[s[lo]] < 0:
                need[s[lo]] += 1
                lo += 1
            if hi - lo < best_len:
                best_lo, best_len = lo, hi - lo
            need[s[lo]] += 1
            missing += 1
            lo += 1
    return "" if best_len == float("inf") else s[best_lo:best_lo + best_len]


def min_subarray_len(target, nums):
    lo, total, best = 0, 0, float("inf")
    for hi, x in enumerate(nums):
        total += x
        while total >= target:
            best = min(best, hi - lo + 1)
            total -= nums[lo]
            lo += 1
    return 0 if best == float("inf") else best


if __name__ == "__main__":
    assert window_max([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert window_max([4, 2], 1) == [4, 2]
    assert window_max([9, 8, 7, 6], 4) == [9]
    assert longest_unique_substring("abcabcbb") == 3
    assert longest_unique_substring("bbbbb") == 1
    assert longest_unique_substring("pwwkew") == 3
    assert longest_unique_substring("") == 0
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "aa") == ""
    assert min_subarray_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert min_subarray_len(100, [1, 2, 3]) == 0
    print("algo_63 sliding window: all tests passed")

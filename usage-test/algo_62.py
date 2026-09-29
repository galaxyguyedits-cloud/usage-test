"""Two-pointer techniques.

- two_sum on a sorted array: move pointers inward based on the sum
- three_sum: sort, fix one element, run two-pointer on the rest
- container with most water: move the shorter wall inward
- remove duplicates in place from a sorted array
- trapping rain water with left/right running maxima
Time: O(n) each (O(n^2) for three_sum). Space: O(1) extra.
"""


def two_sum_sorted(arr, target):
    """Return (i, j) with i < j and arr[i] + arr[j] == target, or None."""
    i, j = 0, len(arr) - 1
    while i < j:
        s = arr[i] + arr[j]
        if s == target:
            return i, j
        if s < target:
            i += 1
        else:
            j -= 1
    return None


def three_sum(nums):
    """All unique triplets summing to zero."""
    nums = sorted(nums)
    res = []
    for k in range(len(nums) - 2):
        if k and nums[k] == nums[k - 1]:
            continue
        i, j = k + 1, len(nums) - 1
        while i < j:
            s = nums[k] + nums[i] + nums[j]
            if s < 0:
                i += 1
            elif s > 0:
                j -= 1
            else:
                res.append([nums[k], nums[i], nums[j]])
                i += 1
                while i < j and nums[i] == nums[i - 1]:
                    i += 1
                j -= 1
    return res


def max_area(heights):
    i, j, best = 0, len(heights) - 1, 0
    while i < j:
        best = max(best, (j - i) * min(heights[i], heights[j]))
        if heights[i] < heights[j]:
            i += 1
        else:
            j -= 1
    return best


def dedupe_sorted(arr):
    """Remove duplicates in place; return new length."""
    if not arr:
        return 0
    w = 1
    for r in range(1, len(arr)):
        if arr[r] != arr[w - 1]:
            arr[w] = arr[r]
            w += 1
    return w


def trap_rain(h):
    i, j, lmax, rmax, water = 0, len(h) - 1, 0, 0, 0
    while i < j:
        if h[i] < h[j]:
            lmax = max(lmax, h[i])
            water += lmax - h[i]
            i += 1
        else:
            rmax = max(rmax, h[j])
            water += rmax - h[j]
            j -= 1
    return water


if __name__ == "__main__":
    assert two_sum_sorted([2, 7, 11, 15], 9) == (0, 1)
    assert two_sum_sorted([1, 3, 4, 6, 8], 10) == (2, 3)
    assert two_sum_sorted([1, 2], 10) is None
    assert three_sum([-1, 0, 1, 2, -1, -4]) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    a = [1, 1, 2, 3, 3, 3, 4]
    n = dedupe_sorted(a)
    assert a[:n] == [1, 2, 3, 4]
    assert trap_rain([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap_rain([4, 2, 0, 3, 2, 5]) == 9
    print("algo_62 two pointers: all tests passed")

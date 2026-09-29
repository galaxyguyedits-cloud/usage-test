"""Boyer-Moore majority vote algorithm.

Finds the element occurring more than n/2 times (if any) in one pass
with O(1) extra space: keep a candidate and a counter, incrementing for
matches and decrementing otherwise; a second pass verifies. The
generalisation finds all elements occurring more than n/3 times.
Time: O(n). Space: O(1).
"""


def majority_element(nums):
    """Return the element appearing > len(nums)/2 times, or None."""
    candidate, count = None, 0
    for x in nums:
        if count == 0:
            candidate, count = x, 1
        elif x == candidate:
            count += 1
        else:
            count -= 1
    if candidate is not None and nums.count(candidate) * 2 > len(nums):
        return candidate
    return None


def majority_n3(nums):
    """Return all elements appearing more than len(nums)/3 times."""
    c1, c2, n1, n2 = None, None, 0, 0
    for x in nums:
        if x == c1:
            n1 += 1
        elif x == c2:
            n2 += 1
        elif n1 == 0:
            c1, n1 = x, 1
        elif n2 == 0:
            c2, n2 = x, 1
        else:
            n1 -= 1
            n2 -= 1
    result = []
    for c in (c1, c2):
        if c is not None and c not in result and nums.count(c) * 3 > len(nums):
            result.append(c)
    return sorted(result)


def brute_majority(nums, frac):
    from collections import Counter
    return sorted(x for x, n in Counter(nums).items() if n * frac > len(nums))


if __name__ == "__main__":
    import random

    assert majority_element([3, 2, 3]) == 3
    assert majority_element([2, 2, 1, 1, 1, 2, 2]) == 2
    assert majority_element([1, 2, 3]) is None
    assert majority_element([]) is None
    assert majority_element([1, 1, 2, 2]) is None
    assert majority_n3([3, 2, 3]) == [3]
    assert majority_n3([1, 1, 1, 3, 3, 2, 2, 2]) == [1, 2]
    assert majority_n3([1]) == [1]
    rnd = random.Random(1)
    for _ in range(300):
        arr = [rnd.randint(0, 3) for _ in range(rnd.randint(0, 12))]
        maj = brute_majority(arr, 2)
        assert majority_element(arr) == (maj[0] if maj else None)
        assert majority_n3(arr) == brute_majority(arr, 3)
    print("algo_71 Boyer-Moore majority vote: all tests passed")

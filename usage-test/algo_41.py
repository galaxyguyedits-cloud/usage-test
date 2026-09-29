"""Sieve of Eratosthenes.

Generates all primes up to n by iteratively marking multiples of each
prime starting at its square. Also includes a smallest-prime-factor
sieve (for fast factorisation) and a segmented sieve for a range.
Time: O(n log log n). Space: O(n).
"""

import math


def sieve(n):
    """Return the list of primes <= n."""
    if n < 2:
        return []
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0
    for p in range(2, math.isqrt(n) + 1):
        if is_prime[p]:
            is_prime[p * p::p] = bytearray(len(range(p * p, n + 1, p)))
    return [i for i, flag in enumerate(is_prime) if flag]


def smallest_prime_factors(n):
    """spf[i] = smallest prime dividing i (spf[0]=spf[1]=0)."""
    spf = list(range(n + 1))
    if n >= 1:
        spf[1] = 0
    spf[0] = 0
    for p in range(2, math.isqrt(n) + 1):
        if spf[p] == p:
            for m in range(p * p, n + 1, p):
                if spf[m] == m:
                    spf[m] = p
    return spf


def segmented_sieve(lo, hi):
    """Return primes in [lo, hi]."""
    base = sieve(math.isqrt(hi))
    mark = [True] * (hi - lo + 1)
    for p in base:
        start = max(p * p, ((lo + p - 1) // p) * p)
        for m in range(start, hi + 1, p):
            mark[m - lo] = False
    return [lo + i for i, ok in enumerate(mark) if ok and lo + i >= 2]


if __name__ == "__main__":
    assert sieve(1) == []
    assert sieve(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert len(sieve(1000)) == 168
    assert len(sieve(100000)) == 9592
    spf = smallest_prime_factors(100)
    assert spf[84] == 2 and spf[91] == 7 and spf[97] == 97
    assert segmented_sieve(100, 130) == [101, 103, 107, 109, 113, 127]
    assert segmented_sieve(0, 10) == [2, 3, 5, 7]
    print("algo_41 sieve of Eratosthenes: all tests passed")

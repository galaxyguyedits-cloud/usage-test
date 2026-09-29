"""Fibonacci numbers: several algorithms.

- naive recursion with memoisation, O(n)
- iterative, O(n) time / O(1) space
- fast doubling, O(log n) using
  F(2k) = F(k) * (2F(k+1) - F(k)),  F(2k+1) = F(k)^2 + F(k+1)^2
- Pisano period for Fibonacci numbers modulo m.
"""

from functools import lru_cache


@lru_cache(maxsize=None)
def fib_memo(n):
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)


def fib_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _fib_pair(n, mod):
    """Return (F(n), F(n+1)) modulo mod (mod None means exact)."""
    if n == 0:
        return 0, 1
    a, b = _fib_pair(n >> 1, mod)
    c = a * (2 * b - a)
    d = a * a + b * b
    if mod:
        c %= mod
        d %= mod
    if n & 1:
        return (d, (c + d) % mod if mod else c + d)
    return c, d


def fib_fast(n, mod=None):
    """F(n) via fast doubling, optionally modulo mod."""
    return _fib_pair(n, mod)[0]


def pisano_period(m):
    """Period of the Fibonacci sequence modulo m (m >= 2)."""
    a, b = 0, 1
    for i in range(1, 6 * m + 1):
        a, b = b, (a + b) % m
        if a == 0 and b == 1:
            return i
    raise RuntimeError("period not found")


if __name__ == "__main__":
    first = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    assert [fib_iter(i) for i in range(11)] == first
    assert [fib_memo(i) for i in range(11)] == first
    assert [fib_fast(i) for i in range(11)] == first
    for n in (50, 100, 321):
        assert fib_fast(n) == fib_iter(n)
    assert fib_fast(5000, 1_000_000_007) == fib_iter(5000) % 1_000_000_007
    assert fib_fast(1000, 97) == fib_iter(1000) % 97
    assert pisano_period(2) == 3 and pisano_period(10) == 60
    assert fib_fast(1000, 10) == fib_fast(1000 % 60, 10)
    print("algo_45 Fibonacci: all tests passed")

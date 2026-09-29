"""Integer prime factorisation.

Trial division by 2 and odd numbers up to sqrt(n), plus Pollard's rho
(Floyd cycle detection) for larger composites. Derived functions:
divisor count, sum of divisors, and Euler's totient.
Time: O(sqrt n) trial division; roughly O(n^(1/4)) for rho.
"""

import math


def trial_factor(n):
    """Return dict prime -> exponent for n >= 1."""
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def _is_prime(n):
    return n >= 2 and all(n % p for p in range(2, math.isqrt(n) + 1))


def pollard_rho(n):
    """Return a non-trivial factor of composite n."""
    if n % 2 == 0:
        return 2
    for c in range(1, n):
        f = lambda x: (x * x + c) % n  # noqa: E731
        x = y = 2
        d = 1
        while d == 1:
            x, y = f(x), f(f(y))
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d
    return n


def factor(n):
    """Return sorted list of prime factors with multiplicity."""
    if n == 1:
        return []
    if _is_prime(n):
        return [n]
    d = pollard_rho(n)
    return sorted(factor(d) + factor(n // d))


def num_divisors(n):
    return math.prod(e + 1 for e in trial_factor(n).values())


def sum_divisors(n):
    return math.prod((p ** (e + 1) - 1) // (p - 1) for p, e in trial_factor(n).items())


def totient(n):
    result = n
    for p in trial_factor(n):
        result -= result // p
    return result


if __name__ == "__main__":
    assert trial_factor(360) == {2: 3, 3: 2, 5: 1}
    assert trial_factor(97) == {97: 1}
    assert trial_factor(1) == {}
    assert factor(8051) == [83, 97]
    assert factor(600851475143) == [71, 839, 1471, 6857]
    assert factor(1024) == [2] * 10
    assert num_divisors(36) == 9 and sum_divisors(28) == 56
    assert totient(36) == 12 and totient(13) == 12
    print("algo_46 prime factorisation: all tests passed")

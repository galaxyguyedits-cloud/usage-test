"""Miller-Rabin primality test.

Writes n-1 = d * 2^s and checks, for each witness a, that either
a^d ≡ 1 (mod n) or a^(d*2^r) ≡ -1 for some r < s. With the fixed
witness set below the test is deterministic for all n < 3.3 * 10^24.
Time: O(k log^3 n). Space: O(1).
"""

WITNESSES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)


def is_probable_prime(n):
    if n < 2:
        return False
    for p in WITNESSES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in WITNESSES:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False  # a is a witness to compositeness
    return True


def trial_division(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def next_prime(n):
    """Smallest prime strictly greater than n."""
    candidate = n + 1
    while not is_probable_prime(candidate):
        candidate += 1
    return candidate


if __name__ == "__main__":
    for n in range(0, 2000):
        assert is_probable_prime(n) == trial_division(n), n
    # Carmichael numbers fool Fermat's test but not Miller-Rabin.
    for c in (561, 1105, 1729, 2465, 2821, 6601, 8911):
        assert not is_probable_prime(c)
    assert is_probable_prime(2 ** 61 - 1)
    assert not is_probable_prime(2 ** 61 + 1)
    assert is_probable_prime(1_000_000_007)
    assert next_prime(100) == 101 and next_prime(13) == 17
    print("algo_44 Miller-Rabin: all tests passed")

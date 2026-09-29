"""Euclidean algorithm and extensions.

GCD via repeated remainders, the extended Euclidean algorithm (which
also finds Bezout coefficients x, y with ax + by = gcd), modular inverse,
LCM, and solving a linear Diophantine equation.
Time: O(log min(a, b)). Space: O(1).
"""


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return 0 if a == 0 or b == 0 else abs(a * b) // gcd(a, b)


def extended_gcd(a, b):
    """Return (g, x, y) such that a*x + b*y == g == gcd(a, b)."""
    old_r, r = a, b
    old_x, x = 1, 0
    old_y, y = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_x, x = x, old_x - q * x
        old_y, y = y, old_y - q * y
    return old_r, old_x, old_y


def mod_inverse(a, m):
    """Return x with a*x ≡ 1 (mod m); raise ValueError if none exists."""
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse modulo {m}")
    return x % m


def solve_diophantine(a, b, c):
    """Return one integer solution (x, y) of ax + by = c, or None."""
    g, x, y = extended_gcd(a, b)
    if c % g:
        return None
    k = c // g
    return x * k, y * k


if __name__ == "__main__":
    assert gcd(48, 18) == 6
    assert gcd(0, 5) == 5 and gcd(-12, 8) == 4
    assert lcm(4, 6) == 12 and lcm(0, 3) == 0
    for a, b in [(240, 46), (99, 78), (17, 5), (1, 1)]:
        g, x, y = extended_gcd(a, b)
        assert g == gcd(a, b) and a * x + b * y == g
    assert mod_inverse(3, 11) == 4
    assert (mod_inverse(17, 3120) * 17) % 3120 == 1
    try:
        mod_inverse(6, 9)
        assert False
    except ValueError:
        pass
    x, y = solve_diophantine(15, 10, 35)
    assert 15 * x + 10 * y == 35
    assert solve_diophantine(4, 6, 5) is None
    print("algo_42 Euclid / extended GCD: all tests passed")

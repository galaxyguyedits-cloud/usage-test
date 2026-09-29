"""Karatsuba multiplication.

Multiplies two n-digit integers with three recursive multiplications of
half-size numbers instead of four:
    x = a*B + b,  y = c*B + d
    x*y = ac*B^2 + ((a+b)(c+d) - ac - bd)*B + bd
Also includes schoolbook digit-list multiplication for comparison.
Time: O(n^log2(3)) ≈ O(n^1.585). Space: O(n).
"""


def karatsuba(x, y, threshold=16):
    """Multiply integers x and y using Karatsuba's algorithm."""
    if x < 0 or y < 0:
        sign = -1 if (x < 0) ^ (y < 0) else 1
        return sign * karatsuba(abs(x), abs(y), threshold)
    if x < threshold or y < threshold:
        return x * y
    n = max(x.bit_length(), y.bit_length())
    half = n // 2
    mask = (1 << half) - 1
    a, b = x >> half, x & mask
    c, d = y >> half, y & mask
    ac = karatsuba(a, c, threshold)
    bd = karatsuba(b, d, threshold)
    mid = karatsuba(a + b, c + d, threshold) - ac - bd
    return (ac << (2 * half)) + (mid << half) + bd


def schoolbook(x_digits, y_digits):
    """Multiply numbers given as little-endian decimal digit lists."""
    res = [0] * (len(x_digits) + len(y_digits))
    for i, xd in enumerate(x_digits):
        carry = 0
        for j, yd in enumerate(y_digits):
            total = res[i + j] + xd * yd + carry
            res[i + j], carry = total % 10, total // 10
        res[i + len(y_digits)] += carry
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


def to_digits(n):
    return [int(ch) for ch in reversed(str(n))]


def from_digits(ds):
    return int("".join(map(str, reversed(ds))))


if __name__ == "__main__":
    import random

    assert karatsuba(1234, 5678) == 7006652
    assert karatsuba(0, 999999) == 0
    assert karatsuba(-12345, 6789) == -12345 * 6789
    assert karatsuba(-3, -4) == 12
    rnd = random.Random(7)
    for _ in range(50):
        a = rnd.getrandbits(rnd.randint(1, 600))
        b = rnd.getrandbits(rnd.randint(1, 600))
        assert karatsuba(a, b) == a * b
        assert karatsuba(a, b, threshold=2) == a * b
    assert from_digits(schoolbook(to_digits(1234), to_digits(5678))) == 7006652
    assert from_digits(schoolbook(to_digits(0), to_digits(55))) == 0
    print("algo_68 Karatsuba: all tests passed")

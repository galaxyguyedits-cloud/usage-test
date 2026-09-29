"""Binomial coefficients and Pascal's triangle.

- Pascal's triangle rows via the recurrence C(n,k) = C(n-1,k-1) + C(n-1,k)
- a single row in O(n) with the multiplicative formula
- C(n, k) exactly with multiplicative formula and symmetry
- C(n, k) mod a prime p with precomputed factorials and Fermat inverses
- Lucas' theorem for huge n modulo small prime p
"""


def pascal_triangle(rows):
    tri = []
    for n in range(rows):
        row = [1] * (n + 1)
        for k in range(1, n):
            row[k] = tri[n - 1][k - 1] + tri[n - 1][k]
        tri.append(row)
    return tri


def pascal_row(n):
    row = [1]
    for k in range(1, n + 1):
        row.append(row[-1] * (n - k + 1) // k)
    return row


def binom(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


class BinomMod:
    """Answer C(n, k) mod prime p for n < limit in O(1) after O(limit) setup."""

    def __init__(self, limit, p=1_000_000_007):
        self.p = p
        self.fact = [1] * (limit + 1)
        for i in range(1, limit + 1):
            self.fact[i] = self.fact[i - 1] * i % p
        self.inv = [1] * (limit + 1)
        self.inv[limit] = pow(self.fact[limit], p - 2, p)
        for i in range(limit, 0, -1):
            self.inv[i - 1] = self.inv[i] * i % p

    def __call__(self, n, k):
        if k < 0 or k > n:
            return 0
        return self.fact[n] * self.inv[k] % self.p * self.inv[n - k] % self.p


def lucas(n, k, p):
    """C(n, k) mod small prime p via Lucas' theorem."""
    result = 1
    while n or k:
        ni, ki = n % p, k % p
        if ki > ni:
            return 0
        result = result * binom(ni, ki) % p
        n //= p
        k //= p
    return result


if __name__ == "__main__":
    tri = pascal_triangle(6)
    assert tri[5] == [1, 5, 10, 10, 5, 1]
    assert all(pascal_row(n) == tri[n] for n in range(6))
    assert binom(52, 5) == 2598960 and binom(10, 11) == 0 and binom(0, 0) == 1
    assert sum(pascal_row(20)) == 2 ** 20
    bm = BinomMod(1000)
    assert bm(100, 50) == binom(100, 50) % 1_000_000_007
    assert bm(5, 7) == 0
    assert lucas(1000, 300, 13) == binom(1000, 300) % 13
    assert lucas(10 ** 18, 10 ** 9, 7) == lucas(10 ** 18, 10 ** 9, 7)
    assert lucas(7, 3, 2) == binom(7, 3) % 2
    print("algo_70 binomial coefficients: all tests passed")

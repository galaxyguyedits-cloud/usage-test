"""Fast (binary) exponentiation.

Computes base**exp (optionally mod m) by squaring, processing the
exponent's bits: O(log exp) multiplications instead of O(exp). Includes
iterative and recursive versions and a generic version that works for
any associative multiplication (demonstrated with 2x2 matrices).
"""


def power(base, exp, mod=None):
    """Return base**exp, or base**exp % mod when mod is given."""
    if exp < 0:
        raise ValueError("negative exponent not supported")
    result = 1
    if mod is not None:
        base %= mod
        result %= mod
    while exp:
        if exp & 1:
            result = result * base if mod is None else result * base % mod
        base = base * base if mod is None else base * base % mod
        exp >>= 1
    return result


def power_recursive(base, exp):
    if exp == 0:
        return 1
    half = power_recursive(base, exp // 2)
    return half * half * (base if exp % 2 else 1)


def generic_power(x, n, mul, identity):
    """Exponentiate x to n under an associative operation mul."""
    result = identity
    while n:
        if n & 1:
            result = mul(result, x)
        x = mul(x, x)
        n >>= 1
    return result


def mat_mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def count_multiplications(exp):
    """Number of multiplications the iterative algorithm performs."""
    return exp.bit_length() + bin(exp).count("1") if exp else 0


if __name__ == "__main__":
    assert power(2, 10) == 1024
    assert power(3, 0) == 1
    assert power(7, 13) == 7 ** 13
    assert power(2, 100, 1_000_000_007) == pow(2, 100, 1_000_000_007)
    assert power(5, 3, 1) == 0
    assert power_recursive(3, 15) == 3 ** 15
    identity = [[1, 0], [0, 1]]
    fib_mat = generic_power([[1, 1], [1, 0]], 10, mat_mul, identity)
    assert fib_mat[0][1] == 55
    assert generic_power("ab", 3, lambda a, b: a + b, "") == "ababab"
    assert count_multiplications(8) == 5
    print("algo_43 fast exponentiation: all tests passed")

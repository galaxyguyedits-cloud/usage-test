"""Newton-Raphson method and square roots.

Newton's method iterates x_{k+1} = x_k - f(x_k)/f'(x_k), converging
quadratically near a simple root. Applied to f(x) = x^2 - a it gives the
Babylonian square root. Also an exact integer square root (Newton on
integers) and bisection as a robust fallback.
"""


def newton(f, df, x0, tol=1e-12, max_iter=100):
    """Find a root of f starting from x0."""
    x = x0
    for _ in range(max_iter):
        d = df(x)
        if d == 0:
            raise ZeroDivisionError("zero derivative")
        step = f(x) / d
        x -= step
        if abs(step) < tol:
            return x
    raise RuntimeError("did not converge")


def sqrt_newton(a, tol=1e-12):
    if a < 0:
        raise ValueError("negative input")
    if a == 0:
        return 0.0
    return newton(lambda x: x * x - a, lambda x: 2 * x, max(a, 1.0), tol)


def isqrt(n):
    """Largest integer r with r*r <= n, using integer Newton iteration."""
    if n < 0:
        raise ValueError("negative input")
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + 1) // 2)  # initial guess >= sqrt(n)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


def bisection(f, lo, hi, tol=1e-12):
    """Root of continuous f on [lo, hi] where f(lo), f(hi) differ in sign."""
    if f(lo) * f(hi) > 0:
        raise ValueError("root not bracketed")
    while hi - lo > tol:
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


if __name__ == "__main__":
    import math

    for a in (2, 9, 0.25, 1e6, 12345.678):
        assert abs(sqrt_newton(a) - math.sqrt(a)) < 1e-9
    assert sqrt_newton(0) == 0.0
    for n in list(range(200)) + [10 ** 30, 10 ** 30 - 1, 2 ** 127]:
        assert isqrt(n) == math.isqrt(n)
    cube_root = newton(lambda x: x ** 3 - 27, lambda x: 3 * x * x, 5.0)
    assert abs(cube_root - 3) < 1e-9
    r = bisection(lambda x: math.cos(x) - x, 0, 1)
    assert abs(math.cos(r) - r) < 1e-9
    try:
        sqrt_newton(-1)
        assert False
    except ValueError:
        pass
    print("algo_69 Newton's method: all tests passed")

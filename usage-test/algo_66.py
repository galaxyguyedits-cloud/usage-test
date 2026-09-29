"""Number base conversion.

Converts integers between bases 2..36 via repeated division (to a base)
and Horner's method (from a base). Also Roman numerals, two's-complement
representation for a fixed bit width, and bit counting.
Time: O(log_b n). Space: O(log_b n).
"""

DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"


def to_base(n, base):
    if not 2 <= base <= 36:
        raise ValueError("base must be in 2..36")
    if n == 0:
        return "0"
    sign = "-" if n < 0 else ""
    n = abs(n)
    out = []
    while n:
        n, r = divmod(n, base)
        out.append(DIGITS[r])
    return sign + "".join(reversed(out))


def from_base(s, base):
    s = s.strip().lower()
    sign = -1 if s.startswith("-") else 1
    value = 0
    for ch in s.lstrip("-"):
        d = DIGITS.index(ch)
        if d >= base:
            raise ValueError(f"digit {ch!r} invalid in base {base}")
        value = value * base + d  # Horner's method
    return sign * value


ROMAN = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
         (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
         (5, "V"), (4, "IV"), (1, "I")]


def to_roman(n):
    out = []
    for value, sym in ROMAN:
        q, n = divmod(n, value)
        out.append(sym * q)
    return "".join(out)


def from_roman(s):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, ch in enumerate(s):
        v = vals[ch]
        total += -v if i + 1 < len(s) and vals[s[i + 1]] > v else v
    return total


def twos_complement(n, bits):
    return format(n & ((1 << bits) - 1), f"0{bits}b")


if __name__ == "__main__":
    assert to_base(255, 16) == "ff" and to_base(255, 2) == "11111111"
    assert to_base(0, 7) == "0" and to_base(-42, 10) == "-42"
    for n in (0, 1, 35, 36, 12345, -9999):
        for b in (2, 3, 8, 16, 36):
            assert from_base(to_base(n, b), b) == n
            if b in (2, 8, 16):
                assert from_base(to_base(n, b), b) == int(to_base(n, b), b)
    try:
        from_base("129", 8)
        assert False
    except ValueError:
        pass
    assert to_roman(1994) == "MCMXCIV" and from_roman("MCMXCIV") == 1994
    assert all(from_roman(to_roman(i)) == i for i in range(1, 4000))
    assert twos_complement(-1, 8) == "11111111" and twos_complement(5, 4) == "0101"
    print("algo_66 base conversion: all tests passed")

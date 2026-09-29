"""Run-length encoding (RLE) and the look-and-say sequence.

RLE compresses runs of repeated symbols into (count, symbol) pairs.
Provides a pair-list form, a compact string form ("3a2b"), and decoders
for both. The look-and-say sequence is RLE applied to its own output.
Time: O(n). Space: O(n).
"""

import re


def rle_pairs(s):
    """Return a list of (symbol, run_length) pairs."""
    pairs = []
    for ch in s:
        if pairs and pairs[-1][0] == ch:
            pairs[-1][1] += 1
        else:
            pairs.append([ch, 1])
    return [tuple(p) for p in pairs]


def rle_encode(s):
    """Encode as count+char, e.g. 'aaab' -> '3a1b'."""
    return "".join(f"{n}{ch}" for ch, n in rle_pairs(s))


def rle_decode(encoded):
    """Inverse of rle_encode (symbols must not be digits)."""
    return "".join(ch * int(n) for n, ch in re.findall(r"(\d+)(\D)", encoded))


def pairs_decode(pairs):
    return "".join(ch * n for ch, n in pairs)


def look_and_say(n):
    """Return the first n terms of the look-and-say sequence from '1'."""
    terms = ["1"]
    while len(terms) < n:
        terms.append(rle_encode(terms[-1]))
    return terms[:n]


def compression_ratio(s):
    enc = rle_encode(s)
    return len(enc) / len(s) if s else 1.0


if __name__ == "__main__":
    assert rle_pairs("aaabccdddd") == [("a", 3), ("b", 1), ("c", 2), ("d", 4)]
    assert rle_encode("aaabccdddd") == "3a1b2c4d"
    assert rle_encode("") == ""
    assert rle_decode("3a1b2c4d") == "aaabccdddd"
    assert rle_decode("12x") == "x" * 12
    for s in ("WWWWWWWWWWWWBWWWWWWWWWWWWBBB", "abc", "zzzzzzzzzzzzzzzz"):
        assert rle_decode(rle_encode(s)) == s
        assert pairs_decode(rle_pairs(s)) == s
    assert look_and_say(6) == ["1", "11", "21", "1211", "111221", "312211"]
    assert compression_ratio("a" * 100) == 0.04
    assert compression_ratio("abcd") == 2.0
    print("algo_65 run-length encoding: all tests passed")

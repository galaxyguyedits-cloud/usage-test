"""Huffman coding.

Builds an optimal prefix-free binary code from symbol frequencies by
repeatedly merging the two least frequent trees (priority queue). Common
symbols get short codes. Includes encoding and decoding.
Time: O(n log n) for n distinct symbols. Space: O(n).
"""

import heapq
from collections import Counter
from itertools import count


def build_codes(text):
    """Return dict symbol -> bit string for the given text."""
    freq = Counter(text)
    if not freq:
        return {}
    if len(freq) == 1:
        return {next(iter(freq)): "0"}
    tie = count()  # tiebreaker so heap never compares trees
    heap = [(f, next(tie), sym) for sym, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        f1, _, a = heapq.heappop(heap)
        f2, _, b = heapq.heappop(heap)
        heapq.heappush(heap, (f1 + f2, next(tie), (a, b)))
    codes = {}

    def walk(node, prefix):
        if isinstance(node, tuple):
            walk(node[0], prefix + "0")
            walk(node[1], prefix + "1")
        else:
            codes[node] = prefix

    walk(heap[0][2], "")
    return codes


def encode(text, codes):
    return "".join(codes[ch] for ch in text)


def decode(bits, codes):
    reverse = {v: k for k, v in codes.items()}
    out, buf = [], ""
    for b in bits:
        buf += b
        if buf in reverse:
            out.append(reverse[buf])
            buf = ""
    if buf:
        raise ValueError("trailing bits do not form a code")
    return "".join(out)


def is_prefix_free(codes):
    words = sorted(codes.values())
    return all(not b.startswith(a) for a, b in zip(words, words[1:]))


if __name__ == "__main__":
    text = "this is an example of a huffman tree"
    codes = build_codes(text)
    assert is_prefix_free(codes)
    bits = encode(text, codes)
    assert decode(bits, codes) == text
    assert len(bits) == 135  # optimal total length for this sentence
    assert len(bits) < 8 * len(text)
    freq = Counter(text)
    assert len(codes[" "]) <= len(codes["x"])
    assert build_codes("aaaa") == {"a": "0"}
    assert decode(encode("aaaa", {"a": "0"}), {"a": "0"}) == "aaaa"
    assert build_codes("") == {}
    assert freq["e"] == 4
    print("algo_64 Huffman coding: all tests passed")

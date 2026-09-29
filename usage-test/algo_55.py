"""Hash map with open addressing (linear probing).

Keys are hashed to a slot; collisions probe the next slot until an
empty one is found. Deletions leave a tombstone so probe chains stay
intact. The table doubles when the load factor exceeds 2/3.
Time: O(1) expected per operation. Space: O(capacity).
"""

_EMPTY = object()
_TOMBSTONE = object()


class OpenAddressingMap:
    def __init__(self, capacity=8):
        self._keys = [_EMPTY] * capacity
        self._vals = [None] * capacity
        self._size = 0
        self._used = 0  # live entries + tombstones

    def _probe(self, key):
        """Yield slot indices along the probe sequence for key."""
        cap = len(self._keys)
        i = hash(key) % cap
        for _ in range(cap):
            yield i
            i = (i + 1) % cap

    def _resize(self, new_cap):
        items = list(self.items())
        self._keys = [_EMPTY] * new_cap
        self._vals = [None] * new_cap
        self._size = self._used = 0
        for k, v in items:
            self[k] = v

    def __setitem__(self, key, value):
        if (self._used + 1) * 3 > len(self._keys) * 2:
            self._resize(len(self._keys) * 2)
        first_tomb = None
        for i in self._probe(key):
            k = self._keys[i]
            if k is _EMPTY:
                target = first_tomb if first_tomb is not None else i
                if target == i:
                    self._used += 1
                self._keys[target], self._vals[target] = key, value
                self._size += 1
                return
            if k is _TOMBSTONE:
                if first_tomb is None:
                    first_tomb = i
            elif k == key:
                self._vals[i] = value
                return

    def _find(self, key):
        for i in self._probe(key):
            k = self._keys[i]
            if k is _EMPTY:
                return None
            if k is not _TOMBSTONE and k == key:
                return i
        return None

    def __getitem__(self, key):
        i = self._find(key)
        if i is None:
            raise KeyError(key)
        return self._vals[i]

    def __delitem__(self, key):
        i = self._find(key)
        if i is None:
            raise KeyError(key)
        self._keys[i], self._vals[i] = _TOMBSTONE, None
        self._size -= 1

    def __contains__(self, key):
        return self._find(key) is not None

    def __len__(self):
        return self._size

    def items(self):
        for k, v in zip(self._keys, self._vals):
            if k is not _EMPTY and k is not _TOMBSTONE:
                yield k, v


if __name__ == "__main__":
    m = OpenAddressingMap()
    for i in range(100):
        m[f"k{i}"] = i
    assert len(m) == 100 and m["k42"] == 42
    m["k42"] = -1
    assert m["k42"] == -1 and len(m) == 100
    for i in range(0, 100, 2):
        del m[f"k{i}"]
    assert len(m) == 50 and "k2" not in m and "k3" in m
    m["k2"] = 2
    assert m["k2"] == 2 and dict(m.items())["k99"] == 99
    try:
        m["missing"]
        assert False
    except KeyError:
        pass
    print("algo_55 open-addressing hash map: all tests passed")

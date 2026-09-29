"""Circular buffer (ring buffer) deque.

A fixed-size array with head index and length; indices wrap around with
modulo arithmetic. Supports push/pop at both ends in O(1) and grows by
doubling when full. Also a sliding-window moving average built on a
bounded ring buffer.
"""


class RingDeque:
    def __init__(self, capacity=4):
        self._buf = [None] * capacity
        self._head = 0
        self._len = 0

    def __len__(self):
        return self._len

    def _grow(self):
        old = list(self)
        self._buf = old + [None] * len(old)
        self._head = 0

    def append(self, x):
        if self._len == len(self._buf):
            self._grow()
        self._buf[(self._head + self._len) % len(self._buf)] = x
        self._len += 1

    def appendleft(self, x):
        if self._len == len(self._buf):
            self._grow()
        self._head = (self._head - 1) % len(self._buf)
        self._buf[self._head] = x
        self._len += 1

    def pop(self):
        if not self._len:
            raise IndexError("pop from empty deque")
        self._len -= 1
        i = (self._head + self._len) % len(self._buf)
        x, self._buf[i] = self._buf[i], None
        return x

    def popleft(self):
        if not self._len:
            raise IndexError("pop from empty deque")
        x, self._buf[self._head] = self._buf[self._head], None
        self._head = (self._head + 1) % len(self._buf)
        self._len -= 1
        return x

    def __iter__(self):
        for i in range(self._len):
            yield self._buf[(self._head + i) % len(self._buf)]


class MovingAverage:
    """Average of the last `size` values using a bounded ring buffer."""

    def __init__(self, size):
        self.buf = [0.0] * size
        self.count = self.idx = 0
        self.total = 0.0

    def next(self, val):
        if self.count == len(self.buf):
            self.total -= self.buf[self.idx]
        else:
            self.count += 1
        self.buf[self.idx] = val
        self.total += val
        self.idx = (self.idx + 1) % len(self.buf)
        return self.total / self.count


if __name__ == "__main__":
    d = RingDeque(2)
    for i in range(5):
        d.append(i)
    d.appendleft(-1)
    assert list(d) == [-1, 0, 1, 2, 3, 4]
    assert d.pop() == 4 and d.popleft() == -1
    assert list(d) == [0, 1, 2, 3] and len(d) == 4
    for _ in range(4):
        d.popleft()
    try:
        d.pop()
        assert False
    except IndexError:
        pass
    ma = MovingAverage(3)
    assert [ma.next(v) for v in (1, 10, 3, 5)] == [1.0, 5.5, 14 / 3, 6.0]
    print("algo_56 ring buffer deque: all tests passed")

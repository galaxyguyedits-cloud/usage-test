"""Queue implemented with two stacks.

Enqueue pushes onto an `inbox` stack; dequeue pops from an `outbox`
stack, refilling it by reversing the inbox only when it is empty. Each
element is moved at most once, giving amortised O(1) operations.
Also includes a max-queue built on the same idea.
"""


class TwoStackQueue:
    def __init__(self, items=()):
        self._in = []
        self._out = []
        for x in items:
            self.enqueue(x)

    def enqueue(self, x):
        self._in.append(x)

    def _shift(self):
        if not self._out:
            while self._in:
                self._out.append(self._in.pop())

    def dequeue(self):
        self._shift()
        if not self._out:
            raise IndexError("dequeue from empty queue")
        return self._out.pop()

    def peek(self):
        self._shift()
        return self._out[-1] if self._out else None

    def __len__(self):
        return len(self._in) + len(self._out)


class MaxQueue:
    """Queue supporting O(1) amortised max() via two max-tracking stacks."""

    def __init__(self):
        self._in = []   # (value, running max)
        self._out = []

    def enqueue(self, x):
        m = max(x, self._in[-1][1]) if self._in else x
        self._in.append((x, m))

    def dequeue(self):
        if not self._out:
            while self._in:
                v, _ = self._in.pop()
                m = max(v, self._out[-1][1]) if self._out else v
                self._out.append((v, m))
        return self._out.pop()[0]

    def max(self):
        cands = [s[-1][1] for s in (self._in, self._out) if s]
        return max(cands)


if __name__ == "__main__":
    q = TwoStackQueue([1, 2, 3])
    assert q.dequeue() == 1
    q.enqueue(4)
    assert q.peek() == 2
    assert [q.dequeue() for _ in range(3)] == [2, 3, 4]
    assert len(q) == 0 and q.peek() is None
    try:
        q.dequeue()
        assert False
    except IndexError:
        pass
    mq = MaxQueue()
    for v in [3, 1, 4, 1, 5]:
        mq.enqueue(v)
    assert mq.max() == 5
    assert mq.dequeue() == 3 and mq.max() == 5
    print("algo_48 two-stack queue: all tests passed")

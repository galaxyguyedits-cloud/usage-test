"""Binary min-heap / priority queue.

Array-backed complete binary tree where each parent <= its children.
push sifts up, pop swaps root with last element then sifts down.
Also merges k sorted lists with the heap.
Time: O(log n) push/pop, O(1) peek, O(n) heapify. Space: O(n).
"""


class MinHeap:
    def __init__(self, items=()):
        self._a = list(items)
        for i in range(len(self._a) // 2 - 1, -1, -1):
            self._sift_down(i)

    def __len__(self):
        return len(self._a)

    def peek(self):
        return self._a[0]

    def push(self, x):
        self._a.append(x)
        self._sift_up(len(self._a) - 1)

    def pop(self):
        a = self._a
        if not a:
            raise IndexError("pop from empty heap")
        a[0], a[-1] = a[-1], a[0]
        top = a.pop()
        if a:
            self._sift_down(0)
        return top

    def _sift_up(self, i):
        a = self._a
        while i > 0:
            p = (i - 1) // 2
            if a[i] < a[p]:
                a[i], a[p] = a[p], a[i]
                i = p
            else:
                break

    def _sift_down(self, i):
        a, n = self._a, len(self._a)
        while True:
            smallest = i
            for c in (2 * i + 1, 2 * i + 2):
                if c < n and a[c] < a[smallest]:
                    smallest = c
            if smallest == i:
                return
            a[i], a[smallest] = a[smallest], a[i]
            i = smallest


def merge_k_sorted(lists):
    heap = MinHeap((lst[0], i, 0) for i, lst in enumerate(lists) if lst)
    out = []
    while len(heap):
        val, i, j = heap.pop()
        out.append(val)
        if j + 1 < len(lists[i]):
            heap.push((lists[i][j + 1], i, j + 1))
    return out


if __name__ == "__main__":
    h = MinHeap([5, 3, 8, 1])
    h.push(0)
    h.push(7)
    assert h.peek() == 0
    assert [h.pop() for _ in range(len(h))] == [0, 1, 3, 5, 7, 8]
    try:
        h.pop()
        assert False
    except IndexError:
        pass
    import random
    rnd = random.Random(42)
    data = [rnd.randint(-100, 100) for _ in range(200)]
    h2 = MinHeap(data)
    assert [h2.pop() for _ in range(len(data))] == sorted(data)
    assert merge_k_sorted([[1, 4, 7], [2, 5], [], [0, 9]]) == [0, 1, 2, 4, 5, 7, 9]
    print("algo_51 min-heap: all tests passed")

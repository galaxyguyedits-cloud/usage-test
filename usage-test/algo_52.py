"""LRU (least recently used) cache.

Combines a hash map (key -> node) with a doubly linked list ordered by
recency. get moves the node to the front; put inserts at the front and
evicts from the back when capacity is exceeded. Sentinel head/tail
nodes remove edge cases.
Time: O(1) get and put. Space: O(capacity).
"""


class _Node:
    __slots__ = ("key", "val", "prev", "next")

    def __init__(self, key=None, val=None):
        self.key, self.val = key, val
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.map = {}
        self.head, self.tail = _Node(), _Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key, default=None):
        node = self.map.get(key)
        if node is None:
            return default
        self._unlink(node)
        self._push_front(node)
        return node.val

    def put(self, key, val):
        node = self.map.get(key)
        if node:
            node.val = val
            self._unlink(node)
        else:
            if len(self.map) == self.capacity:
                lru = self.tail.prev
                self._unlink(lru)
                del self.map[lru.key]
            node = _Node(key, val)
            self.map[key] = node
        self._push_front(node)

    def keys(self):
        """Keys from most to least recently used."""
        out, cur = [], self.head.next
        while cur is not self.tail:
            out.append(cur.key)
            cur = cur.next
        return out


if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, "one")
    c.put(2, "two")
    assert c.get(1) == "one"        # 1 becomes most recent
    c.put(3, "three")               # evicts 2
    assert c.get(2) is None
    assert c.keys() == [3, 1]
    c.put(1, "uno")                 # update moves to front
    c.put(4, "four")                # evicts 3
    assert c.get(3) is None and c.get(1) == "uno" and c.get(4) == "four"
    assert len(c.map) == 2
    try:
        LRUCache(0)
        assert False
    except ValueError:
        pass
    print("algo_52 LRU cache: all tests passed")

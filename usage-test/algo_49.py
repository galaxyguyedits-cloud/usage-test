"""Singly linked list.

Nodes hold a value and a pointer to the next node. Supports append,
prepend, delete, search, in-place reversal, middle-node lookup with
slow/fast pointers, and merging two sorted lists.
Append is O(1) with a tail pointer; search/delete are O(n).
"""


class Node:
    __slots__ = ("val", "next")

    def __init__(self, val, nxt=None):
        self.val = val
        self.next = nxt


class LinkedList:
    def __init__(self, items=()):
        self.head = self.tail = None
        self.size = 0
        for x in items:
            self.append(x)

    def append(self, val):
        node = Node(val)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self.size += 1

    def prepend(self, val):
        self.head = Node(val, self.head)
        if self.tail is None:
            self.tail = self.head
        self.size += 1

    def delete(self, val):
        """Remove first node with value val; return True if removed."""
        prev, cur = None, self.head
        while cur and cur.val != val:
            prev, cur = cur, cur.next
        if cur is None:
            return False
        if prev:
            prev.next = cur.next
        else:
            self.head = cur.next
        if cur is self.tail:
            self.tail = prev
        self.size -= 1
        return True

    def reverse(self):
        prev, cur = None, self.head
        self.tail = cur
        while cur:
            cur.next, prev, cur = prev, cur, cur.next
        self.head = prev

    def middle(self):
        slow = fast = self.head
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
        return slow.val if slow else None

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.val
            cur = cur.next


def merge_sorted(a, b):
    out = LinkedList()
    x, y = a.head, b.head
    while x and y:
        if x.val <= y.val:
            out.append(x.val)
            x = x.next
        else:
            out.append(y.val)
            y = y.next
    for rest in (x, y):
        while rest:
            out.append(rest.val)
            rest = rest.next
    return out


if __name__ == "__main__":
    ll = LinkedList([1, 2, 3, 4])
    ll.prepend(0)
    assert list(ll) == [0, 1, 2, 3, 4] and ll.size == 5
    assert ll.delete(4) and not ll.delete(42)
    ll.append(9)
    assert list(ll) == [0, 1, 2, 3, 9] and ll.middle() == 2
    ll.reverse()
    assert list(ll) == [9, 3, 2, 1, 0]
    ll.append(-1)
    assert ll.tail.val == -1
    m = merge_sorted(LinkedList([1, 4, 6]), LinkedList([2, 3, 7, 8]))
    assert list(m) == [1, 2, 3, 4, 6, 7, 8]
    print("algo_49 linked list: all tests passed")

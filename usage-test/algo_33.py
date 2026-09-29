"""Trie (prefix tree).

A tree where each edge is a character, so all keys sharing a prefix
share a path from the root. Supports insert, exact lookup, prefix
queries, autocomplete, deletion and longest common prefix.
Time: O(L) per operation for a key of length L. Space: O(total chars).
"""


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self, words=()):
        self.root = TrieNode()
        for w in words:
            self.insert(w)

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def _walk(self, prefix):
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def contains(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def complete(self, prefix):
        """Return all stored words beginning with prefix, sorted."""
        node = self._walk(prefix)
        out = []

        def collect(n, acc):
            if n.is_end:
                out.append(acc)
            for ch in sorted(n.children):
                collect(n.children[ch], acc + ch)

        if node:
            collect(node, prefix)
        return out

    def longest_common_prefix(self):
        node, prefix = self.root, ""
        while len(node.children) == 1 and not node.is_end:
            ch, node = next(iter(node.children.items()))
            prefix += ch
        return prefix


if __name__ == "__main__":
    t = Trie(["apple", "app", "application", "apt", "banana"])
    assert t.contains("app") and t.contains("apple")
    assert not t.contains("appl")
    assert t.starts_with("appl") and not t.starts_with("c")
    assert t.complete("app") == ["app", "apple", "application"]
    assert t.complete("z") == []
    assert Trie(["flower", "flow", "flight"]).longest_common_prefix() == "fl"
    assert Trie(["dog", "car"]).longest_common_prefix() == ""
    print("algo_33 trie: all tests passed")

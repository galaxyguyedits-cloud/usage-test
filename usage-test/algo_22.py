"""Kruskal's minimum spanning tree with a disjoint-set union.

Sorts edges by weight and greedily adds each edge that connects two
different components, tracked by a union-find structure with path
compression and union by rank.
Time: O(E log E). Space: O(V).
"""


class DisjointSet:
    """Union-find with path compression and union by rank."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal(vertices, edges):
    """Return (total_weight, mst_edges) for an undirected graph.

    edges is a list of (weight, u, v). If the graph is disconnected a
    minimum spanning forest is returned.
    """
    ds = DisjointSet(vertices)
    mst, total = [], 0
    for w, u, v in sorted(edges):
        if ds.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == len(vertices) - 1:
                break
    return total, mst


if __name__ == "__main__":
    ds = DisjointSet(range(5))
    assert ds.union(0, 1) and ds.union(3, 4)
    assert not ds.union(1, 0)
    assert ds.find(0) == ds.find(1) and ds.find(2) != ds.find(3)
    V = "ABCDEFG"
    E = [(7, "A", "B"), (5, "A", "D"), (8, "B", "C"), (9, "B", "D"),
         (7, "B", "E"), (5, "C", "E"), (15, "D", "E"), (6, "D", "F"),
         (8, "E", "F"), (9, "E", "G"), (11, "F", "G")]
    total, mst = kruskal(V, E)
    assert total == 39
    assert len(mst) == 6
    t2, m2 = kruskal("abcd", [(1, "a", "b"), (2, "c", "d")])
    assert t2 == 3 and len(m2) == 2
    print("algo_22 Kruskal MST: all tests passed")

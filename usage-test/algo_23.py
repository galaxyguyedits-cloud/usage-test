"""Prim's minimum spanning tree algorithm.

Grows the MST from a start vertex, always adding the cheapest edge that
connects the tree to a vertex not yet in it. Uses a lazy binary heap.
Time: O(E log V). Space: O(V + E).
"""

import heapq


def prim(graph, start):
    """Return (total_weight, mst_edges) for the component containing start.

    graph maps vertex -> list of (neighbour, weight) (undirected: each
    edge should appear in both adjacency lists).
    """
    visited = {start}
    heap = [(w, start, v) for v, w in graph.get(start, [])]
    heapq.heapify(heap)
    mst, total = [], 0
    while heap and len(visited) < len(graph):
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        mst.append((u, v, w))
        total += w
        for nxt, w2 in graph.get(v, []):
            if nxt not in visited:
                heapq.heappush(heap, (w2, v, nxt))
    return total, mst


def build_undirected(edge_list):
    """Build an adjacency dict from (u, v, w) triples."""
    g = {}
    for u, v, w in edge_list:
        g.setdefault(u, []).append((v, w))
        g.setdefault(v, []).append((u, w))
    return g


def prim_matrix(matrix):
    """O(V^2) Prim on an adjacency matrix (0 means no edge). Returns weight."""
    n = len(matrix)
    in_tree = [False] * n
    key = [float("inf")] * n
    key[0] = 0
    total = 0
    for _ in range(n):
        u = min((k, i) for i, k in enumerate(key) if not in_tree[i])[1]
        in_tree[u] = True
        total += key[u]
        for v in range(n):
            if matrix[u][v] and not in_tree[v] and matrix[u][v] < key[v]:
                key[v] = matrix[u][v]
    return total


if __name__ == "__main__":
    edges = [("A", "B", 2), ("A", "D", 6), ("B", "C", 3), ("B", "D", 8),
             ("B", "E", 5), ("C", "E", 7), ("D", "E", 9)]
    g = build_undirected(edges)
    total, mst = prim(g, "A")
    assert total == 16
    assert len(mst) == 4
    assert prim(g, "E")[0] == 16
    m = [[0, 2, 0, 6, 0], [2, 0, 3, 8, 5], [0, 3, 0, 0, 7],
         [6, 8, 0, 0, 9], [0, 5, 7, 9, 0]]
    assert prim_matrix(m) == 16
    assert prim({"solo": []}, "solo") == (0, [])
    print("algo_23 Prim MST: all tests passed")

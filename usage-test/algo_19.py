"""Dijkstra's shortest path algorithm.

Computes single-source shortest paths in a graph with non-negative edge
weights using a binary heap priority queue. Also reconstructs the path
to a chosen target.
Time: O((V + E) log V). Space: O(V).
"""

import heapq


def dijkstra(graph, source):
    """Return (dist, prev) dicts for all vertices reachable from source.

    graph maps vertex -> list of (neighbour, weight).
    """
    dist = {source: 0}
    prev = {source: None}
    heap = [(0, source)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in graph.get(u, []):
            if w < 0:
                raise ValueError("negative edge weight")
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def shortest_path(graph, source, target):
    """Return (cost, path) from source to target, or (inf, []) if none."""
    dist, prev = dijkstra(graph, source)
    if target not in dist:
        return float("inf"), []
    path, node = [], target
    while node is not None:
        path.append(node)
        node = prev[node]
    return dist[target], path[::-1]


if __name__ == "__main__":
    g = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 5), ("D", 10)],
        "C": [("E", 3)],
        "D": [("F", 11)],
        "E": [("D", 4)],
        "F": [],
        "Z": [("A", 1)],
    }
    dist, _ = dijkstra(g, "A")
    assert dist == {"A": 0, "B": 4, "C": 2, "E": 5, "D": 9, "F": 20}
    assert shortest_path(g, "A", "D") == (9, ["A", "C", "E", "D"])
    assert shortest_path(g, "A", "Z") == (float("inf"), [])
    assert shortest_path(g, "A", "A") == (0, ["A"])
    try:
        dijkstra({"a": [("b", -1)]}, "a")
        assert False
    except ValueError:
        pass
    print("algo_19 Dijkstra: all tests passed")

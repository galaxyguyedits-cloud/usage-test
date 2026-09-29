"""Bellman-Ford algorithm.

Single-source shortest paths that tolerates negative edge weights.
Relaxes every edge V-1 times; a further successful relaxation proves a
negative-weight cycle reachable from the source.
Time: O(V * E). Space: O(V).
"""

INF = float("inf")


def bellman_ford(vertices, edges, source):
    """Return dict of shortest distances from source.

    edges is a list of (u, v, weight). Raises ValueError if a negative
    cycle is reachable from source.
    """
    dist = {v: INF for v in vertices}
    dist[source] = 0
    for _ in range(len(vertices) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            raise ValueError("graph contains a negative-weight cycle")
    return dist


def has_negative_cycle(vertices, edges):
    """Detect a negative cycle anywhere using a virtual super-source."""
    src = object()
    extra = [(src, v, 0) for v in vertices]
    try:
        bellman_ford(list(vertices) + [src], edges + extra, src)
        return False
    except ValueError:
        return True


if __name__ == "__main__":
    V = ["S", "A", "B", "C", "D"]
    E = [
        ("S", "A", 6), ("S", "B", 7), ("A", "C", 5), ("A", "D", -4),
        ("A", "B", 8), ("B", "C", -3), ("B", "D", 9), ("C", "A", -2),
        ("D", "S", 2), ("D", "C", 7),
    ]
    d = bellman_ford(V, E, "S")
    assert d == {"S": 0, "A": 2, "B": 7, "C": 4, "D": -2}
    assert not has_negative_cycle(V, E)
    bad = [("x", "y", 1), ("y", "z", -3), ("z", "x", 1)]
    assert has_negative_cycle(["x", "y", "z"], bad)
    iso = bellman_ford(["p", "q"], [], "p")
    assert iso == {"p": 0, "q": INF}
    print("algo_20 Bellman-Ford: all tests passed")

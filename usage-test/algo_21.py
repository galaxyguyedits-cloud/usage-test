"""Floyd-Warshall algorithm.

All-pairs shortest paths via dynamic programming: for each intermediate
vertex k, update dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]).
Keeps a `nxt` matrix for path reconstruction.
Time: O(V^3). Space: O(V^2).
"""

INF = float("inf")


def floyd_warshall(n, edges):
    """Return (dist, nxt) matrices for vertices 0..n-1.

    edges is a list of (u, v, w) directed edges.
    """
    dist = [[INF] * n for _ in range(n)]
    nxt = [[None] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        nxt[i][i] = i
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
            nxt[u][v] = v
    for k in range(n):
        for i in range(n):
            if dist[i][k] == INF:
                continue
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt


def reconstruct(nxt, u, v):
    """Return path from u to v using the nxt matrix ([] if unreachable)."""
    if nxt[u][v] is None:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path


def transitive_closure(n, edges):
    """reach[i][j] is True iff j is reachable from i."""
    dist, _ = floyd_warshall(n, [(u, v, 1) for u, v in edges])
    return [[dist[i][j] != INF for j in range(n)] for i in range(n)]


if __name__ == "__main__":
    edges = [(0, 1, 3), (0, 2, 8), (1, 2, 2), (2, 3, 1), (3, 0, 4), (1, 3, 7)]
    dist, nxt = floyd_warshall(4, edges)
    assert dist[0] == [0, 3, 5, 6]
    assert dist[3] == [4, 7, 9, 0]
    assert reconstruct(nxt, 0, 3) == [0, 1, 2, 3]
    assert reconstruct(nxt, 2, 1) == [2, 3, 0, 1]
    d2, n2 = floyd_warshall(3, [(0, 1, 1)])
    assert d2[1][0] == INF and reconstruct(n2, 1, 0) == []
    reach = transitive_closure(3, [(0, 1), (1, 2)])
    assert reach[0][2] and not reach[2][0]
    print("algo_21 Floyd-Warshall: all tests passed")

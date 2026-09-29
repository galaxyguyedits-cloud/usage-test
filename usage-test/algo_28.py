"""Cycle detection in directed and undirected graphs.

Directed: DFS with three colours; reaching a GRAY (on-stack) vertex
means a back edge, i.e. a cycle. The cycle itself is reconstructed.
Undirected: union-find; an edge joining two already-connected vertices
closes a cycle.
Time: O(V + E). Space: O(V).
"""


def find_directed_cycle(graph):
    """Return a list of vertices forming a cycle (first == last), or None."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in graph}
    parent = {}

    def dfs(u):
        color[u] = GRAY
        for v in graph.get(u, []):
            if color.get(v, WHITE) == GRAY:
                cycle = [v, u]
                while u != v:
                    u = parent[u]
                    cycle.append(u)
                return cycle[::-1]
            if color.get(v, WHITE) == WHITE:
                parent[v] = u
                found = dfs(v)
                if found:
                    return found
        color[u] = BLACK
        return None

    for v in graph:
        if color[v] == WHITE:
            found = dfs(v)
            if found:
                return found
    return None


def has_undirected_cycle(n, edges):
    """Union-find cycle check for undirected graph on 0..n-1."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return True
        parent[ru] = rv
    return False


if __name__ == "__main__":
    g = {0: [1], 1: [2], 2: [3], 3: [1], 4: []}
    cyc = find_directed_cycle(g)
    assert cyc[0] == cyc[-1]
    assert set(cyc) == {1, 2, 3}
    for a, b in zip(cyc, cyc[1:]):
        assert b in g[a]
    assert find_directed_cycle({0: [1], 1: [2], 2: []}) is None
    assert find_directed_cycle({0: [0]}) == [0, 0]
    assert has_undirected_cycle(3, [(0, 1), (1, 2), (2, 0)])
    assert not has_undirected_cycle(4, [(0, 1), (1, 2), (2, 3)])
    print("algo_28 cycle detection: all tests passed")

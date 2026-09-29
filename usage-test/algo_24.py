"""Topological sort.

Orders the vertices of a directed acyclic graph so that every edge u->v
has u before v. Implements Kahn's algorithm (BFS on in-degrees) and a
DFS-based variant. Both detect cycles.
Time: O(V + E). Space: O(V).
"""

from collections import deque


def kahn_toposort(graph):
    """Return a topological order, raising ValueError on a cycle."""
    indeg = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            indeg[v] = indeg.get(v, 0) + 1
    queue = deque(sorted(v for v, d in indeg.items() if d == 0))
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph.get(u, []):
            indeg[v] -= 1
            if indeg[v] == 0:
                queue.append(v)
    if len(order) != len(indeg):
        raise ValueError("graph has a cycle")
    return order


def dfs_toposort(graph):
    """DFS-based topological sort (reverse postorder)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}
    out = []

    def visit(u):
        color[u] = GRAY
        for v in graph.get(u, []):
            c = color.get(v, WHITE)
            if c == GRAY:
                raise ValueError("graph has a cycle")
            if c == WHITE:
                visit(v)
        color[u] = BLACK
        out.append(u)

    for u in graph:
        if color.get(u, WHITE) == WHITE:
            visit(u)
    return out[::-1]


def is_valid_order(graph, order):
    pos = {v: i for i, v in enumerate(order)}
    return all(pos[u] < pos[v] for u in graph for v in graph[u])


if __name__ == "__main__":
    dag = {
        "shirt": ["tie", "belt"], "tie": ["jacket"], "pants": ["shoes", "belt"],
        "belt": ["jacket"], "socks": ["shoes"], "shoes": [], "jacket": [],
        "undershorts": ["pants", "shoes"],
    }
    k = kahn_toposort(dag)
    d = dfs_toposort(dag)
    assert is_valid_order(dag, k) and is_valid_order(dag, d)
    assert len(k) == len(dag) == len(d)
    assert kahn_toposort({1: [2], 2: [3], 3: []}) == [1, 2, 3]
    for fn in (kahn_toposort, dfs_toposort):
        try:
            fn({1: [2], 2: [3], 3: [1]})
            assert False
        except ValueError:
            pass
    print("algo_24 topological sort: all tests passed")

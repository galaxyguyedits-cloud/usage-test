"""Bipartite graph check (two-colouring).

A graph is bipartite iff its vertices can be coloured with two colours
so no edge joins vertices of the same colour, equivalently iff it has no
odd cycle. Uses BFS colouring over every component.
Time: O(V + E). Space: O(V).
"""

from collections import deque


def two_color(graph):
    """Return a dict vertex -> 0/1 colouring, or None if not bipartite."""
    color = {}
    for s in graph:
        if s in color:
            continue
        color[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in graph.get(u, []):
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    return None
    return color


def is_bipartite(graph):
    return two_color(graph) is not None


def partitions(graph):
    """Return the two vertex sets (left, right) or None."""
    col = two_color(graph)
    if col is None:
        return None
    left = {v for v, c in col.items() if c == 0}
    right = {v for v, c in col.items() if c == 1}
    return left, right


def cycle_graph(n):
    """Undirected cycle on vertices 0..n-1."""
    return {i: [(i - 1) % n, (i + 1) % n] for i in range(n)}


if __name__ == "__main__":
    assert is_bipartite(cycle_graph(4))
    assert is_bipartite(cycle_graph(6))
    assert not is_bipartite(cycle_graph(3))
    assert not is_bipartite(cycle_graph(5))
    k23 = {"a": [1, 2, 3], "b": [1, 2, 3], 1: ["a", "b"],
           2: ["a", "b"], 3: ["a", "b"]}
    left, right = partitions(k23)
    assert {frozenset(left), frozenset(right)} == {
        frozenset("ab"), frozenset({1, 2, 3})
    }
    col = two_color(k23)
    assert all(col[u] != col[v] for u in k23 for v in k23[u])
    assert is_bipartite({})
    assert is_bipartite({1: [], 2: []})
    print("algo_27 bipartite check: all tests passed")

"""Breadth-first search (BFS).

Explores a graph level by level from a source vertex using a FIFO queue.
Finds shortest paths (by edge count) in unweighted graphs and can be
used to compute connected components.
Time: O(V + E). Space: O(V).
"""

from collections import deque


def bfs_order(graph, start):
    """Return vertices in the order BFS visits them from start."""
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in graph.get(node, []):
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    return order


def shortest_path(graph, start, goal):
    """Return the shortest path (list of vertices) or None if unreachable."""
    parent = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parent[node]
            return path[::-1]
        for nb in graph.get(node, []):
            if nb not in parent:
                parent[nb] = node
                queue.append(nb)
    return None


def connected_components(graph):
    """Return a list of sets, one per connected component (undirected)."""
    seen, comps = set(), []
    for v in graph:
        if v not in seen:
            comp = set(bfs_order(graph, v))
            seen |= comp
            comps.append(comp)
    return comps


if __name__ == "__main__":
    g = {
        "A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
        "D": ["B"], "E": ["B", "F"], "F": ["C", "E"],
        "X": ["Y"], "Y": ["X"],
    }
    assert bfs_order(g, "A") == ["A", "B", "C", "D", "E", "F"]
    assert shortest_path(g, "A", "F") == ["A", "C", "F"]
    assert shortest_path(g, "D", "F") == ["D", "B", "E", "F"]
    assert shortest_path(g, "A", "X") is None
    assert shortest_path(g, "A", "A") == ["A"]
    comps = connected_components(g)
    assert len(comps) == 2 and {"X", "Y"} in comps
    print("algo_17 BFS: all tests passed")

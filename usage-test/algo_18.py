"""Depth-first search (DFS).

Explores a graph as deep as possible along each branch before
backtracking. Provides recursive and iterative traversals plus
path finding and pre/post-order timestamps.
Time: O(V + E). Space: O(V).
"""


def dfs_recursive(graph, start, visited=None, order=None):
    """Return vertices in recursive DFS preorder from start."""
    if visited is None:
        visited, order = set(), []
    visited.add(start)
    order.append(start)
    for nb in graph.get(start, []):
        if nb not in visited:
            dfs_recursive(graph, nb, visited, order)
    return order


def dfs_iterative(graph, start):
    """Iterative DFS producing the same order as the recursive version."""
    visited, order, stack = set(), [], [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        # Reverse so the first neighbour is processed first.
        for nb in reversed(graph.get(node, [])):
            if nb not in visited:
                stack.append(nb)
    return order


def find_path(graph, start, goal, path=None):
    """Return some path from start to goal via DFS, or None."""
    path = (path or []) + [start]
    if start == goal:
        return path
    for nb in graph.get(start, []):
        if nb not in path:
            found = find_path(graph, nb, goal, path)
            if found:
                return found
    return None


def timestamps(graph, start):
    """Return dicts of discovery and finish times for reachable vertices."""
    disc, fin, clock = {}, {}, [0]

    def visit(u):
        disc[u] = clock[0]
        clock[0] += 1
        for v in graph.get(u, []):
            if v not in disc:
                visit(v)
        fin[u] = clock[0]
        clock[0] += 1

    visit(start)
    return disc, fin


if __name__ == "__main__":
    g = {1: [2, 3], 2: [4, 5], 3: [6], 4: [], 5: [6], 6: []}
    assert dfs_recursive(g, 1) == [1, 2, 4, 5, 6, 3]
    assert dfs_iterative(g, 1) == dfs_recursive(g, 1)
    assert find_path(g, 1, 6) == [1, 2, 5, 6]
    assert find_path(g, 4, 1) is None
    d, f = timestamps(g, 1)
    assert d[1] == 0 and f[1] == 11
    assert d[2] < d[4] < f[4] < f[2]
    print("algo_18 DFS: all tests passed")

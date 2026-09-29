"""Tarjan's strongly connected components.

Single DFS pass that assigns each vertex a discovery index and a
low-link value (smallest index reachable via the DFS subtree plus at
most one back edge). A vertex whose low-link equals its index is the
root of an SCC, which is popped off an explicit stack.
Time: O(V + E). Space: O(V).
"""

import sys


def tarjan_scc(graph):
    """Return a list of SCCs (each a sorted list) of a directed graph."""
    sys.setrecursionlimit(max(10000, sys.getrecursionlimit()))
    index = {}
    low = {}
    on_stack = set()
    stack = []
    sccs = []
    counter = [0]

    def strongconnect(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, []):
            if w not in index:
                strongconnect(w)
                low[v] = min(low[v], low[w])
            elif w in on_stack:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(sorted(comp))

    for v in graph:
        if v not in index:
            strongconnect(v)
    return sccs


def condensation_size(graph):
    """Number of vertices in the condensation DAG."""
    return len(tarjan_scc(graph))


if __name__ == "__main__":
    g = {
        1: [2], 2: [3], 3: [1, 4], 4: [5], 5: [6], 6: [4, 7], 7: [], 8: [7, 8],
    }
    comps = sorted(tarjan_scc(g))
    assert comps == [[1, 2, 3], [4, 5, 6], [7], [8]]
    assert condensation_size({"a": ["b"], "b": ["a"]}) == 1
    assert condensation_size({"a": ["b"], "b": ["c"], "c": []}) == 3
    # Tarjan emits SCCs in reverse topological order of the condensation.
    order = tarjan_scc({"a": ["b"], "b": ["c"], "c": []})
    assert order == [["c"], ["b"], ["a"]]
    print("algo_25 Tarjan SCC: all tests passed")

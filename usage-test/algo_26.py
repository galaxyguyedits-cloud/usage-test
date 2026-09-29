"""A* search on a grid.

Best-first search that expands nodes in order of f = g + h, where g is
the cost so far and h is an admissible heuristic (Manhattan distance on
a 4-connected grid). Finds optimal paths while exploring fewer nodes
than Dijkstra.
Time: O(E log V) worst case. Space: O(V).
"""

import heapq


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    """Return shortest path of (row, col) cells from start to goal.

    grid is a list of strings; '#' marks walls. Returns None if blocked.
    """
    rows, cols = len(grid), len(grid[0])
    open_heap = [(manhattan(start, goal), 0, start)]
    came_from = {start: None}
    g_score = {start: 0}
    while open_heap:
        _, g, cur = heapq.heappop(open_heap)
        if cur == goal:
            path = []
            while cur is not None:
                path.append(cur)
                cur = came_from[cur]
            return path[::-1]
        if g > g_score[cur]:
            continue  # stale heap entry
        r, c = cur
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                ng = g + 1
                if ng < g_score.get((nr, nc), float("inf")):
                    g_score[(nr, nc)] = ng
                    came_from[(nr, nc)] = cur
                    f = ng + manhattan((nr, nc), goal)
                    heapq.heappush(open_heap, (f, ng, (nr, nc)))
    return None


if __name__ == "__main__":
    maze = [
        "S....",
        ".###.",
        "...#.",
        ".#...",
        "...#G",
    ]
    path = astar(maze, (0, 0), (4, 4))
    assert path[0] == (0, 0) and path[-1] == (4, 4)
    assert len(path) - 1 == 8
    for (r1, c1), (r2, c2) in zip(path, path[1:]):
        assert manhattan((r1, c1), (r2, c2)) == 1
        assert maze[r2][c2] != "#"
    blocked = ["S#", "#G"]
    assert astar(blocked, (0, 0), (1, 1)) is None
    assert astar(["S"], (0, 0), (0, 0)) == [(0, 0)]
    print("algo_26 A* search: all tests passed")

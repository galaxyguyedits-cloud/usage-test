"""Sudoku solver (backtracking with constraint sets).

Maintains the set of digits used in each row, column and 3x3 box.
Always fills the empty cell with the fewest candidates (MRV heuristic),
which prunes the search dramatically.
Worst case exponential, but fast on typical puzzles.
"""


def solve_sudoku(grid):
    """Solve a 9x9 grid in place (0 = empty). Return True if solved."""
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empties = []
    for r in range(9):
        for c in range(9):
            v = grid[r][c]
            if v:
                b = (r // 3) * 3 + c // 3
                if v in rows[r] or v in cols[c] or v in boxes[b]:
                    return False
                rows[r].add(v)
                cols[c].add(v)
                boxes[b].add(v)
            else:
                empties.append((r, c))

    def candidates(r, c):
        return set(range(1, 10)) - rows[r] - cols[c] - boxes[(r // 3) * 3 + c // 3]

    def backtrack():
        if not empties:
            return True
        # MRV: choose the empty cell with fewest candidates.
        idx = min(range(len(empties)), key=lambda i: len(candidates(*empties[i])))
        r, c = empties.pop(idx)
        b = (r // 3) * 3 + c // 3
        for v in candidates(r, c):
            grid[r][c] = v
            rows[r].add(v)
            cols[c].add(v)
            boxes[b].add(v)
            if backtrack():
                return True
            rows[r].remove(v)
            cols[c].remove(v)
            boxes[b].remove(v)
        grid[r][c] = 0
        empties.insert(idx, (r, c))
        return False

    return backtrack()


def is_solved(grid):
    full = set(range(1, 10))
    for i in range(9):
        if set(grid[i]) != full or {grid[r][i] for r in range(9)} != full:
            return False
        br, bc = (i // 3) * 3, (i % 3) * 3
        if {grid[br + dr][bc + dc] for dr in range(3) for dc in range(3)} != full:
            return False
    return True


if __name__ == "__main__":
    puzzle = [
        "530070000", "600195000", "098000060",
        "800060003", "400803001", "700020006",
        "060000280", "000419005", "000080079",
    ]
    grid = [[int(ch) for ch in row] for row in puzzle]
    original = [row[:] for row in grid]
    assert solve_sudoku(grid)
    assert is_solved(grid)
    assert all(original[r][c] in (0, grid[r][c]) for r in range(9) for c in range(9))
    assert grid[0] == [5, 3, 4, 6, 7, 8, 9, 1, 2]
    bad = [row[:] for row in original]
    bad[0][2] = 5  # duplicate 5 in first row
    assert not solve_sudoku(bad)
    print("algo_58 sudoku solver: all tests passed")

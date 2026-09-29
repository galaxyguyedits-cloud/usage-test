"""N-Queens via backtracking.

Place N queens on an N x N board so no two attack each other. Places one
queen per row, tracking occupied columns and both diagonals in sets for
O(1) conflict checks, and backtracks on dead ends. A bitmask variant
counts solutions faster.
Time: O(N!) worst case. Space: O(N).
"""


def solve_n_queens(n):
    """Return all solutions; each is a list of column indices per row."""
    solutions = []
    cols, diag1, diag2 = set(), set(), set()
    placement = []

    def place(row):
        if row == n:
            solutions.append(list(placement))
            return
        for c in range(n):
            if c in cols or (row - c) in diag1 or (row + c) in diag2:
                continue
            cols.add(c)
            diag1.add(row - c)
            diag2.add(row + c)
            placement.append(c)
            place(row + 1)
            placement.pop()
            cols.remove(c)
            diag1.remove(row - c)
            diag2.remove(row + c)

    place(0)
    return solutions


def count_n_queens_bitmask(n):
    full = (1 << n) - 1

    def go(cols, d1, d2):
        if cols == full:
            return 1
        total = 0
        free = full & ~(cols | d1 | d2)
        while free:
            bit = free & -free
            free ^= bit
            total += go(cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1)
        return total

    return go(0, 0, 0)


def render(solution):
    n = len(solution)
    return ["".join("Q" if c == col else "." for c in range(n)) for col in solution]


def is_valid(solution):
    n = len(solution)
    for i in range(n):
        for j in range(i + 1, n):
            if solution[i] == solution[j] or abs(solution[i] - solution[j]) == j - i:
                return False
    return True


if __name__ == "__main__":
    sols4 = solve_n_queens(4)
    assert sorted(sols4) == [[1, 3, 0, 2], [2, 0, 3, 1]]
    assert render([1, 3, 0, 2]) == [".Q..", "...Q", "Q...", "..Q."]
    expected = {1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    for n, cnt in expected.items():
        assert len(solve_n_queens(n)) == cnt
        assert count_n_queens_bitmask(n) == cnt
    assert all(is_valid(s) for s in solve_n_queens(8))
    print("algo_57 N-Queens: all tests passed")

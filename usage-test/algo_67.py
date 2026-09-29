"""Convex hull (Andrew's monotone chain).

Sorts points lexicographically, then builds the lower and upper hulls
with a stack, popping points that would make a non-left (clockwise or
collinear) turn, detected with the 2-D cross product. Also computes the
hull's area (shoelace formula) and point-in-convex-polygon tests.
Time: O(n log n). Space: O(n).
"""


def cross(o, a, b):
    """Z-component of (a - o) x (b - o); > 0 means counter-clockwise turn."""
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points):
    """Return hull vertices in counter-clockwise order, starting lowest-left."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def polygon_area(poly):
    """Area of a simple polygon via the shoelace formula."""
    s = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def inside_convex(poly, p):
    """True if p is inside or on the boundary of CCW convex polygon."""
    n = len(poly)
    return all(cross(poly[i], poly[(i + 1) % n], p) >= 0 for i in range(n))


if __name__ == "__main__":
    pts = [(0, 3), (2, 2), (1, 1), (2, 1), (3, 0), (0, 0), (3, 3), (1, 2)]
    hull = convex_hull(pts)
    assert hull == [(0, 0), (3, 0), (3, 3), (0, 3)]
    assert polygon_area(hull) == 9.0
    assert all(inside_convex(hull, p) for p in pts)
    assert not inside_convex(hull, (4, 1))
    # Collinear points are excluded from the hull.
    assert convex_hull([(0, 0), (1, 1), (2, 2), (3, 3)]) == [(0, 0), (3, 3)]
    assert convex_hull([(1, 1)]) == [(1, 1)]
    tri = convex_hull([(0, 0), (4, 0), (2, 3), (2, 1)])
    assert tri == [(0, 0), (4, 0), (2, 3)] and polygon_area(tri) == 6.0
    print("algo_67 convex hull: all tests passed")

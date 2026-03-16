import numpy as np


def ccw(a, b, c):
    res = np.linalg.det([[a[0], a[1], 1], [b[0], b[1], 1], [c[0], c[1], 1]])
    res = int(round(res))
    return res > 0


def inCircle(a, b, c, d):
    res = np.linalg.det(
        [
            [a[0], a[1], (a[0]) ** 2 + (a[1]) ** 2, 1],
            [b[0], b[1], (b[0]) ** 2 + (b[1]) ** 2, 1],
            [c[0], c[1], (c[0]) ** 2 + (c[1]) ** 2, 1],
            [d[0], d[1], (d[0]) ** 2 + (d[1]) ** 2, 1],
        ]
    )
    res = int(round(res))
    return res > 0


def rightOf(x, e):
    return ccw(x, e.dest, e.org)


def leftOf(x, e):
    return ccw(x, e.org, e.dest)


# e above basel?
def valid(e, basel):
    return ccw(e.dest, basel.dest, basel.org)

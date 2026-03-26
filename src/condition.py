from condition_calc import ccw_int_exact, incircle_int_exact
from point import Point


def ccw(a: Point, b: Point, c: Point):
    return ccw_int_exact(a, b, c)


def incircle(a: Point, b: Point, c: Point, d: Point):
    return incircle_int_exact(a, b, c, d)


def right_of(x: Point, e):
    return ccw(x, e.dest, e.org)


def left_of(x: Point, e):
    return ccw(x, e.org, e.dest)


# e above basel?
def valid(e, basel):
    return ccw(e.dest, basel.dest, basel.org)

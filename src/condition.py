from det import ccw_int_exact
from det import incircle_int_exact


def ccw(a, b, c):
    return ccw_int_exact(a, b, c)


def incircle(a, b, c, d):
    return incircle_int_exact(a, b, c, d)


def right_of(x, e):
    return ccw(x, e.dest, e.org)


def left_of(x, e):
    return ccw(x, e.org, e.dest)


# e above basel?
def valid(e, basel):
    return ccw(e.dest, basel.dest, basel.org)

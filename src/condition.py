from shewchuk import incircle as incircle_c
from shewchuk import ccw as ccw_c


def ccw(a, b, c):
    return ccw_c(a, b, c)


def incircle(a, b, c, d):
    return incircle_c(a, b, c, d)


def right_of(x, e):
    return ccw(x, e.dest, e.org)


def left_of(x, e):
    return ccw(x, e.org, e.dest)


# e above basel?
def valid(e, basel):
    return ccw_c(e.dest, basel.dest, basel.org)

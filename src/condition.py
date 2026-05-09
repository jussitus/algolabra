from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from edge import Edge
from condition_calc import ccw_int_exact, incircle_int_exact
from point import Point


def ccw(a: Point, b: Point, c: Point) -> bool:
    """Tests if the triangle `abc` is oriented counterclockwise.

    CCW test is also known as Orient2D.
    """
    return ccw_int_exact(a, b, c)


def incircle(a: Point, b: Point, c: Point, d: Point) -> bool:
    """Tests if point `d` is inside the circle `abc`."""
    return incircle_int_exact(a, b, c, d)


def right_of(x: Point, e: Edge):
    """Tests if a point is on the right side of the edge."""
    return ccw(x, e.dest, e.org)


def left_of(x: Point, e: Edge):
    """Tests if a point is on the left side of the edge."""
    return ccw(x, e.org, e.dest)


def valid(e: Edge, basel: Edge):
    """Tests if an edge's destination is above a right-to-left base edge."""
    return ccw(e.dest, basel.dest, basel.org)

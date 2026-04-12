from condition import ccw, incircle, left_of, right_of, valid
from edge import make_quad_edge
COLLINEAR_THREE_INT = [(-1, -1), (1, 1), (2, 2)]
COLLINEAR_FOUR_INT = [(-1, -1), (1, 1), (2, 2), (3, 3)]
TRIANGLE_INT_TOP_LEFT_RIGHT = [(1, 1), (-1, 1), (1, 0)]
TRIANGLE_INT_LEFT_RIGHT_TOP = [(-1, -1), (1, -1), (0, 1)]
EDGE = make_quad_edge((0,0), (1,1))
COLLINEAR = (-1,-1) 
LEFT = (0,1)
RIGHT = (1,0)
BASE_LEFT = make_quad_edge((1,1), (0,0))
ABOVE_BASE = make_quad_edge((0,1), (1,2))
BELOW_BASE = make_quad_edge((0,-1), (1,0))
def big(l):
    return [(13**10000 * x, 17**10000 * y) for (x, y) in l]


def test_ccw_collinear_int():
    assert not ccw(*COLLINEAR_THREE_INT)


def test_ccw_collinear_int_big():
    assert not ccw(*big(COLLINEAR_THREE_INT))


def test_incircle_collinear_int():
    assert not incircle(*COLLINEAR_FOUR_INT)


def test_ccw_triangle_from_top_to_left_to_right():
    assert ccw(*TRIANGLE_INT_TOP_LEFT_RIGHT)


def test_ccw_triangle_from_left_to_right_to_top():
    assert ccw(*TRIANGLE_INT_LEFT_RIGHT_TOP)

def test_left_of():
    assert left_of(LEFT, EDGE)

def test_left_of_collinear():
    assert not left_of(COLLINEAR, EDGE)

def test_right_of():
    assert right_of(RIGHT, EDGE)

def test_right_of_collinear():
    assert not right_of(COLLINEAR, EDGE)

def test_valid_above():
    assert valid(ABOVE_BASE, BASE_LEFT)

def test_valid_not_above():
    assert not valid(BELOW_BASE, BASE_LEFT)

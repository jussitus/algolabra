from condition import ccw, incircle, left_of, right_of, valid

COLLINEAR_THREE_INT = [(-1, -1), (1, 1), (2, 2)]
COLLINEAR_FOUR_INT = [(-1, -1), (1, 1), (2, 2), (3, 3)]
COLLINEAR_THREE_FLOAT = [(-0.1, -0.066), (0.1, 0.066), (0.2, 0.132)]
COLLINEAR_FOUR_FLOAT = [(-0.1, -0.066), (0.2, 0.066), (0.2, 0.132), (0.3, 0.198)]
TRIANGLE_INT_TOP_LEFT_RIGHT = [(1, 1), (-1, 1), (1, 0)]
TRIANGLE_INT_LEFT_RIGHT_TOP = [(-1, -1), (1, -1), (0, 1)]

""" 
KESKEN

"""


def big(l):
    return [
        (
            12345678901234567891234567890123456789 * x,
            12345678901234567891234567890123456789 * y,
        )
        for (x, y) in l
    ]


def small(l):
    return [
        (
            x / 12345678901234567891234567890123456789,
            y / 12345678901234567891234567890123456789,
        )
        for (x, y) in l
    ]


def test_ccw_collinear_int():
    assert not ccw(*COLLINEAR_THREE_INT)


def test_ccw_collinear_float():
    assert not ccw(*COLLINEAR_THREE_FLOAT)


def test_ccw_collinear_int_big():
    assert not ccw(*big(COLLINEAR_THREE_INT))


def test_ccw_collinear_float_small():
    assert not ccw(*small(COLLINEAR_THREE_FLOAT))


def test_incircle_collinear_int():
    assert not incircle(*COLLINEAR_FOUR_INT)


def test_incircle_collinear_float():
    assert not incircle(*COLLINEAR_FOUR_FLOAT)


def test_ccw_triangle_from_top_to_left_to_right():
    assert ccw(*TRIANGLE_INT_TOP_LEFT_RIGHT)


def test_ccw_triangle_from_left_to_right_to_top():
    assert ccw(*TRIANGLE_INT_LEFT_RIGHT_TOP)

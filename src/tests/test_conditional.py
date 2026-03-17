from condition import ccw, incircle, left_of, right_of, valid

COLLINEAR_THREE_INT = [(-1, -1), (1, 1), (2, 2)]
COLLINEAR_FOUR_INT = [(-1, -1), (1, 1), (2, 2), (3, 3)]
COLLINEAR_THREE_FLOAT = [(-1.0, -0.66), (1.0, 0.66), (2.0, 1.32)]
COLLINEAR_FOUR_FLOAT = [(-1.0, -0.66), (1.0, 0.66), (2.0, 1.32), (3.0, 1.98)]


def test_ccw_collinear_int():
    assert ccw(*COLLINEAR_THREE_INT) == 0


def test_ccw_collinear_float():
    assert ccw(*COLLINEAR_THREE_FLOAT) == 0

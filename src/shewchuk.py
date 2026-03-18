import ctypes
from pathlib import Path

parent_dir = Path(__file__).parent
so_file = parent_dir / "c" / "shewchuk.so"
_shewchuk = ctypes.CDLL(str(so_file))
_shewchuk.exactinit.argtypes = []
_shewchuk.exactinit.restype = None
_shewchuk.exactinit()
_shewchuk.incircle.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
]
_shewchuk.incircle.restype = ctypes.c_double
_shewchuk.orient2d.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
]
_shewchuk.orient2d.restype = ctypes.c_double

def incircle(a, b, c, d):
    array_type = ctypes.c_double * 2
    res = _shewchuk.incircle(
        array_type(*a), array_type(*b), array_type(*c), array_type(*d)
    )
    return res > 0


def ccw(a, b, c):
    array_type = ctypes.c_double * 2
    res = _shewchuk.orient2d(array_type(*a), array_type(*b), array_type(*c))
    return res > 0

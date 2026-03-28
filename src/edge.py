from math import sqrt
from typing import Any, Self, override
from condition import ccw
from point import Point


class Edge:
    """Class representing a single directed component of a quad-edge.

    In this code 'edge' always refers to one edge component of a quad-edge. The `Edge` class does not implement faces (left, right) or orientation (flip). Face information is encoded in the mathematical structure, however.

    Attributes:
        `org`: A tuple representing the x,y coordinates of the origin of the edge.
        `onext`: The next edge with the same origin (`org`) in the counterclockwise (CCW) direction. These form a ring and repeated invocations of onext will eventually lead back to the same edge.
        `sym`: The symmetric edge, which is the same as the original edge with origin (`org`) and destination (`dest`) swapped.
        `rot`: The edge rotated 90 degrees counterclockwise (CCW). Part of the Voronoi diagram.
        `tor`: The edge rotated 90 degrees clockwise (CW). Same as `self.tor.sym`. Part of the Voronoi diagram.
        `dual`: A boolean indicating if the edge is in the Voronoi diagram. Note that the actual dual is the flipped version, but flip is not implemented.
        `radius`: The radius of the circumcircle centered on `org`. Only defined for Voronoi edges.
    """

    __slots__: list[str] = [
        "org",
        "onext",
        "sym",
        "rot",
        "tor",
        "dual",
        "radius",
        "_length",
        "data",
    ]

    def __init__(self):
        """Initializes the instance.

        Edges are only created in fours by the function `make_quad_edge`, so `self.org`, `self.sym`, `self.rot` and `self.tor` are never None after creation.

        """
        self.org: Point = None  # pyright: ignore[reportAttributeAccessIssue]
        self.sym: Edge = None  # pyright: ignore[reportAttributeAccessIssue]
        self.onext: Edge = self
        self.rot: Edge = None  # pyright: ignore[reportAttributeAccessIssue]
        self.tor: Edge = None  # pyright: ignore[reportAttributeAccessIssue]
        self.dual: bool = False
        self.radius: float | None = None
        self._length: float | None = None
        self.data: Any | None = None

    @property
    def lnext(self) -> "Edge":
        """The next edge with the same left face (`self.tor.onext.rot`) when moving counterclockwise (CCW) around the face."""
        return self.tor.onext.rot

    @property
    def rnext(self) -> "Edge":
        """The next edge with the same right face (`self.rot.onext.tor`) when moving counterclockwise (CCW) around the face."""
        return self.rot.onext.tor

    @property
    def dnext(self) -> "Edge":
        """The next edge with the same destination (`self.dest`) when moving counterclockwise (CCW) around the right face.

        Same as `self.sym.onext.sym`.
        """
        return self.sym.onext.sym

    @property
    def dest(self) -> Point:
        """The destination of the edge, which is the origin of the symmetric edge (`self.sym.org`)."""
        return self.sym.org

    @property
    def oprev(self) -> "Edge":
        """The previous edge with the same origin (`org`) in the counterclockwise (CCW) direction.

        Note: It is the _previous_ edge. It is the next edge in the clockwise (CW) direction. These form a ring and repeated invocations of oprev will eventually lead back to the same edge. Same as `self.rot.onext.rot`.
        """
        return self.rot.onext.rot

    @property
    def rprev(self) -> "Edge":
        """The previous edge with the same right face (`self.sym.onext`) when moving counterclockwise (CCW) around the face.

        Note: It is the _previous_ edge. It is the next edge when moving clockwise (CW) around the face.
        """
        return self.sym.onext

    @property
    def length(self) -> float:
        """Length of the edge.

        Calculated when first accessed. Can be `float('inf')` for outer Voronoi edges.
        """
        if self._length is None:
            if self.sym is None or self.org is None or self.sym.org is None:
                return float("inf")
            self._length = sqrt(
                (self.org[0] - self.dest[0]) ** 2 + (self.org[1] - self.dest[1]) ** 2
            )
        return self._length

    @override
    def __str__(self) -> str:
        if self.sym is None:
            dest = (float("inf"), float("inf"))
        else:
            dest = self.dest
        string = f"Edge({self.org} -> {dest})"
        return string

    def __lt__(self, other: Self) -> bool:
        """Compares the lengths of the edges."""
        return self.length < other.length


def make_quad_edge(org: Point, dest: Point) -> Edge:
    """Doc string to do"""
    e = Edge()
    e_sym = Edge()
    e_rot = Edge()
    e_tor = Edge()

    e.org = org
    e_sym.org = dest

    e.onext = e
    e_sym.onext = e_sym
    e_rot.onext = e_tor
    e_tor.onext = e_rot

    e.sym = e_sym
    e_sym.sym = e
    e_rot.sym = e_tor
    e_tor.sym = e_rot

    e.rot = e_rot
    e_sym.rot = e_tor
    e_rot.rot = e_sym
    e_tor.rot = e

    e.tor = e_tor
    e_sym.tor = e_rot
    e_rot.tor = e
    e_tor.tor = e_sym

    e.dual = False
    e.sym.dual = False
    e_rot.dual = True
    e_tor.dual = True

    return e


def splice(a: Edge, b: Edge):
    """Docstring to do"""
    alpha = a.onext.rot
    beta = b.onext.rot

    alpha.onext, beta.onext = beta.onext, alpha.onext
    a.onext, b.onext = b.onext, a.onext


def connect(a: Edge, b: Edge) -> Edge:
    """Docstring to do"""
    e = make_quad_edge(a.dest, b.org)
    splice(e, a.lnext)
    splice(e.sym, b)
    return e


def delete_quad_edge(e: Edge):
    """Docstring to do"""
    splice(e, e.oprev)
    splice(e.sym, e.sym.oprev)


def triangle_ccw(e: Edge) -> tuple[Edge, Edge, Edge]:
    """Docstring to do"""
    return (e, e.lnext, e.lnext.lnext)


def triangle_cw(e: Edge) -> tuple[Edge, Edge, Edge]:
    """Docstring to do"""
    return (e, e.rnext, e.rnext.rnext)


def circumcircle(e: Edge) -> tuple[Point, float]:
    """Docstring to do"""
    a, b, c = triangle_ccw(e)
    d = 2 * (
        a.org[0] * (b.org[1] - c.org[1])
        + b.org[0] * (c.org[1] - a.org[1])
        + c.org[0] * (a.org[1] - b.org[1])
    )
    x = (1 / d) * (
        (a.org[0] ** 2 + a.org[1] ** 2) * (b.org[1] - c.org[1])
        + (b.org[0] ** 2 + b.org[1] ** 2) * (c.org[1] - a.org[1])
        + (c.org[0] ** 2 + c.org[1] ** 2) * (a.org[1] - b.org[1])
    )
    y = (1 / d) * (
        (a.org[0] ** 2 + a.org[1] ** 2) * (c.org[0] - b.org[0])
        + (b.org[0] ** 2 + b.org[1] ** 2) * (a.org[0] - c.org[0])
        + (c.org[0] ** 2 + c.org[1] ** 2) * (b.org[0] - a.org[0])
    )
    r = sqrt((a.org[0] - x) ** 2 + (a.org[1] - y) ** 2)
    return (x, y), r

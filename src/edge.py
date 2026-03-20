from math import sqrt
from condition import ccw


class Edge:
    """Delaunay triangulaation peruspalikka, placeholder"""

    __slots__ = [
        "org",
        "sym",
        "onext",
        "rot",
        "tor",
        "dual",
        "data",
        "radius",
        "_length",
    ]

    def __init__(self):
        self.org: tuple[int | float, int | float] | None = None
        self.sym: Edge | None = None
        self.onext: Edge | None = self
        self.rot: Edge | None = None
        self.tor: Edge | None = None
        self.dual: bool = False
        self.data = None
        self.radius: float | None = None
        self._length: float | None = None

    @property
    def lnext(self):
        return self.tor.onext.rot

    @property
    def rnext(self):
        return self.rot.onext.tor

    @property
    def dnext(self):
        return self.sym.onext.sym

    @property
    def dest(self):
        return self.sym.org

    @property
    def oprev(self):
        return self.rot.onext.rot

    @property
    def rprev(self):
        return self.sym.onext

    @property
    def length(self):
        if self._length is None:
            if self.org is not None and self.dest is not None:
                self._length = sqrt(
                    (self.org[0] - self.sym.org[0]) ** 2
                    + (self.dest[1] - self.sym.dest[1]) ** 2
                )
            else:
                return float("-Infinity")  # infinite voronoi edge
        return self._length

    def __str__(self):
        string = f"org={self.org}, dest={self.dest}, length={self.length}"
        return string

    def __lt__(self, other):
        return self.length < other.length


def make_quad_edge(org, dest):
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

    e_rot.dual = True
    e_tor.dual = True

    return e


def splice(a, b):
    alpha = a.onext.rot
    beta = b.onext.rot

    alpha.onext, beta.onext = beta.onext, alpha.onext
    a.onext, b.onext = b.onext, a.onext


def connect(a, b) -> Edge:
    e = make_quad_edge(a.dest, b.org)
    splice(e, a.lnext)
    splice(e.sym, b)
    return e


def delete_quad_edge(e):
    splice(e, e.oprev)
    splice(e.sym, e.sym.oprev)


def triangle_ccw(e: Edge) -> tuple[Edge, Edge, Edge]:
    return (e, e.lnext, e.lnext.lnext)


def triangle_cw(e: Edge) -> tuple[Edge, Edge, Edge]:
    return (e, e.rnext, e.rnext.rnext)


def circumcircle(e: Edge):
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


def circumcircles(edges: list[Edge]):
    ccs = set()
    for e in edges:
        if ccw(e.org, e.dest, e.lnext.dest):
            ccs.add(circumcircle(e))
    return ccs

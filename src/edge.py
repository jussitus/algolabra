from math import sqrt
from condition import ccw


class Edge:
    """Delaunay triangulaation peruspalikka, placeholder"""

    def __init_(self):
        self.data = None
        self.org = None
        self.onext: Edge = None
        self.rot: Edge = None

    @property
    def sym(self):
        return self.rot.rot

    @sym.setter
    def sym(self, value):
        self.rot.rot = value

    @property
    def tor(self):
        return self.rot.rot.rot

    @tor.setter
    def tor(self, value):
        self.rot.rot.rot = value

    @property
    def lnext(self):
        return self.tor.onext.rot

    @lnext.setter
    def lnext(self, value):
        self.tor.onext.rot = value

    @property
    def rnext(self):
        return self.rot.onext.tor

    @rnext.setter
    def rnext(self, value):
        self.rot.onext.tor = value

    @property
    def dnext(self):
        return self.sym.onext.sym

    @dnext.setter
    def dnext(self, value):
        self.sym.onext.sym = value

    @property
    def dest(self):
        return self.sym.org

    @dest.setter
    def dest(self, value):
        self.sym.org = value

    @property
    def oprev(self):
        return self.rot.onext.rot

    @oprev.setter
    def oprev(self, value):
        self.rot.onext.rot = value

    @property
    def rprev(self):
        return self.sym.onext

    @rprev.setter
    def rprev(self, value):
        self.sym.onext = value

    def __str__(self):
        return "{" + f"org: {self.org}, dest: {self.dest}" + "}"


def makeQuadEdge(org, dest):
    e = Edge()
    eSym = Edge()
    eRot = Edge()
    eTor = Edge()

    e.org = org
    eSym.org = dest

    e.rot = eRot
    eSym.rot = eTor
    eRot.rot = eSym
    eTor.rot = e

    e.onext = e
    eSym.onext = eSym
    eRot.onext = eTor
    eTor.onext = eRot

    return e


def splice(a, b):
    alpha = a.onext.rot
    beta = b.onext.rot

    alpha.onext, beta.onext = beta.onext, alpha.onext
    a.onext, b.onext = b.onext, a.onext


def connect(a, b) -> Edge:
    e = makeQuadEdge(a.dest, b.org)
    splice(e, a.lnext)
    splice(e.sym, b)
    return e


def deleteEdge(e):
    splice(e, e.oprev)
    splice(e.sym, e.sym.oprev)


def triangle_ccw(e: Edge) -> tuple[Edge]:
    return (e, e.lnext, e.lnext.lnext)


def triangle_cw(e: Edge) -> tuple[Edge]:
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
    circumcircles = set()
    for e in edges:
        if ccw(e.org, e.dest, e.lnext.dest):
            circumcircles.add(circumcircle(e))
    return circumcircles


def hull(e: Edge):
    hull = [e]
    first = e
    current = e.rprev
    while first != current:
        hull.append(current)
        current = current.rprev
    return hull

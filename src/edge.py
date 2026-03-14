

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
    @property
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
        return "{" + f'org: {self.org}, dest: {self.dest}' + "}"

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

def splice(a,b):
    alpha = a.onext.rot
    beta = b.onext.rot

    alpha.onext, beta.onext = beta.onext, alpha.onext
    a.onext, b.onext = b.onext, a.onext


def connect(a, b) -> Edge:
    e = makeQuadEdge(a.dest,b.org)
    e.org = a.dest
    e.dest = b.org
    splice(e, a.lnext)
    splice(e.sym, b)
    return e

def deleteEdge(e):
    splice(e, e.oprev)
    splice(e.sym, e.sym.oprev)




























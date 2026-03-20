from math import sqrt, log
import heapq as hq
from edge import (
    Edge,
    make_quad_edge,
    splice,
    connect,
    delete_quad_edge,
    circumcircle,
    triangle_ccw,
)
from condition import (
    ccw,
    incircle,
    right_of,
    left_of,
    valid,
)
from time import time


class Delaunay:
    def __init__(self, vertices):
        self._vertices = sorted(vertices)
        self._edges = []
        self._left = None
        self._right = None
        self._triangles = []
        self._hull = []
        self._delaunay = []
        self._voronoi = []
        self._mst = []

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def triangles(self):
        if len(self._triangles) > 0 or len(self.edges) == 0:
            return self._triangles
        triangles = []
        for e in self.edges:
            if e.dual or e.sym in self.hull:
                continue
            if e.org[0] <= e.lnext.org[0] and e.org[0] <= e.lnext.lnext.org[0]:
                triangles.append(triangle_ccw(e))
        self._triangles = triangles
        return self._triangles

    @property
    def hull(self):
        if len(self._hull) > 0 or len(self.edges) == 0:
            return self._hull
        hull = [self.left]
        first = self.left
        current = first.rprev
        while first != current:
            hull.append(current)
            current = current.rprev
        self._hull = hull
        return self._hull

    @property
    def delaunay(self):
        return self._delaunay

    @property
    def voronoi(self):
        return self._voronoi

    @property
    def mst(self):
        return self._mst

    def run_prim(self):
        start = time()
        visited = {}
        mst = []
        heap = []

        first = self._delaunay[2]
        hq.heappush(heap, first.sym)
        visited[first.org] = True
        current = first.onext
        while first is not current:
            hq.heappush(heap, current.sym)
            current = current.onext
        while len(heap) > 0:
            first = hq.heappop(heap)
            current = first.onext
            while first is not current:
                if not visited.get(current.dest, False):
                    hq.heappush(heap, current.sym)
                current = current.onext
            if not visited.get(first.org, False):
                mst.append(first)
                visited[first.org] = True
        end = time()
        total = end - start
        n = len(self._vertices)
        ratio = total / (n * log(n))
        print(f"PRIM: n = {n}, ratio = {ratio}, time = {total}")
        print
        self._mst = mst

    def run_delaunay(self):
        self._left, self._right, bad_edges = _delaunay(self._vertices, self._edges, [])
        self._edges = list(set(self.edges) - set(bad_edges))

    def run_voronoi(self):
        for t in self.triangles:
            for e in t:
                vo = e.rot

                if e not in self.hull:
                    org, r_sym = circumcircle(e.sym)
                    vo.sym.radius = r_sym
                else:
                    vo.org = (float("inf"), float("inf"))

                vo.sym.org, r = circumcircle(e)
                vo.radius = r
                vo.sym.radius = r

    def run(self):
        self.run_delaunay()
        self.run_voronoi()

        for e in self.edges:
            if not e.dual and e.org < e.dest:
                self._delaunay.append(e)
                self._voronoi.append(e.rot)

        self.run_prim()


def _delaunay(s, edges, bad_edges):
    if len(s) < 2:
        raise ValueError(f"len(s)={len(s)} is less than 2")
    if len(s) == 2:
        a = make_quad_edge(s[0], s[1])
        edges.extend([a, a.sym, a.rot, a.tor])
        return (a, a.sym, bad_edges)
    if len(s) == 3:
        a = make_quad_edge(s[0], s[1])
        edges.extend([a, a.sym, a.rot, a.tor])
        b = make_quad_edge(s[1], s[2])
        edges.extend([b, b.sym, b.rot, b.tor])
        splice(a.sym, b)
        if ccw(s[0], s[1], s[2]):
            c = connect(b, a)
            edges.extend([c, c.sym, c.rot, c.tor])
            return (a, b.sym, bad_edges)
        if ccw(s[0], s[2], s[1]):
            c = connect(b, a)
            edges.extend([c, c.sym, c.rot, c.tor])
            return (c.sym, c, bad_edges)

        return (a, b.sym, bad_edges)

    mid = len(s) // 2
    (ldo, ldi, lbad_edges) = _delaunay(s[:mid], edges, bad_edges)
    (rdi, rdo, rbad_edges) = _delaunay(s[mid:], edges, bad_edges)
    while True:
        if left_of(rdi.org, ldi):
            ldi = ldi.lnext
        elif right_of(ldi.org, rdi):
            rdi = rdi.rprev
        else:
            break
    basel = connect(rdi.sym, ldi)
    edges.extend([basel, basel.sym, basel.rot, basel.tor])
    if ldi.org == ldo.org:
        ldo = basel.sym
    if rdi.org == rdo.org:
        rdo = basel

    # merge loop
    while True:
        lcand = basel.sym.onext
        if valid(lcand, basel):
            while incircle(basel.dest, basel.org, lcand.dest, lcand.onext.dest):
                t = lcand.onext
                delete_quad_edge(lcand)
                bad_edges.extend([lcand, lcand.sym, lcand.rot, lcand.tor])
                lcand = t
        rcand = basel.oprev

        if valid(rcand, basel):
            while incircle(basel.dest, basel.org, rcand.dest, rcand.oprev.dest):
                t = rcand.oprev
                delete_quad_edge(rcand)
                bad_edges.extend([rcand, rcand.sym, rcand.rot, rcand.tor])
                rcand = t

        if not valid(lcand, basel) and not valid(rcand, basel):
            break

        if not valid(lcand, basel) or (
            valid(rcand, basel)
            and incircle(lcand.dest, lcand.org, rcand.org, rcand.dest)
        ):
            basel = connect(rcand, basel.sym)
            edges.extend([basel, basel.sym, basel.rot, basel.tor])
        else:
            basel = connect(basel.sym, lcand.sym)
            edges.extend([basel, basel.sym, basel.rot, basel.tor])
    return (ldo, rdo, bad_edges)

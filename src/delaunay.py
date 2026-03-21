from math import sqrt
from time import time
from tqdm import tqdm
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
from point import Point


class PlanarGraph:
    """Class representing a planar graph.

    Args:
        vertices: a list of (x,y) points
    """

    def __init__(self, vertices):
        self._vertices: list[tuple[float, float]] = sorted(vertices)
        self._edges: list[Edge] = []
        self._left: Edge | None = None
        self._right: Edge | None = None
        self._triangles: list[list[Edge]] = []
        self._hull: list[Edge] = []
        self._delaunay: list[Edge] = []
        self._voronoi: list[Edge] = []
        self._mst_delaunay: list[Edge] = []
        self._mst_voronoi: list[Edge] = []

    @property
    def vertices(self) -> list[tuple[int | float, int | float]]:
        """Vertices of the graph."""
        return self._vertices

    def extreme_vertices(self) -> dict[str, Point]:
        """A dict of the extreme left, right, bottom, and top vertices."""
        min_x = self.vertices[0]
        max_x = self.vertices[-1]
        min_y = min(self.vertices, key=(lambda v: v[1]))
        max_y = max(self.vertices, key=(lambda v: v[1]))
        return {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}

    @property
    def edges(self) -> list[Edge]:
        """Edges of the graph, including all of the four edges of a quad-edge."""
        return self._edges

    @property
    def left(self) -> Edge | None:
        """Left edge of the Delaunay triangualtion as given by the Guibas-Stolfi divide-and-conquer algorithm.

        The left edge's origin is the leftmost vertex of the graph. It is a hull edge in the counterclockwise direction.
        """
        return self._left

    @property
    def right(self) -> Edge | None:
        """Right edge of the Delaunay Triangulation as given by the Guibas-Stolfi divide-and-conquer algorithm.

        The right edge's origin is the rightmost vertex of the graph. It is a hull edge in the clockwise direction.
        """
        return self._right

    @property
    def triangles(self) -> list[list[Edge]]:
        """Triangles in the Delaunay triangulation.

        Each triangle is a list of three edges in the counterclockwise direction. The list of triangles is populated the first time this property is accessed.
        """
        if len(self._triangles) > 0 or self.left is None:
            return self._triangles
        triangles = []
        for e in self.delaunay:
            a, b, c = triangle_ccw(e)
            if not (a.org < b.org and a.org < c.org):
                continue
            if ccw(a.org, b.org, c.org):
                triangles.append(triangle_ccw(e))
        self._triangles = triangles
        return self._triangles

    @property
    def hull(self) -> list[Edge]:
        """Hull edges of the Delaunay triangulation.

        The list is populated the first time this property is accessed.
        """
        if len(self._hull) > 0 or self.left is None:
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
    def delaunay(self) -> list[Edge]:
        """Edges in the Delaunay triangulation, without their symmetric (Sym) edges."""
        return self._delaunay

    @property
    def voronoi(self) -> list[Edge]:
        """Edges in the Voronoi diagram, without their symmetric (Sym) edges."""
        return self._voronoi

    @property
    def mst_delaunay(self) -> list[Edge]:
        """Edges in the minimum spanning tree of the Delaunay triangulation."""
        return self._mst_delaunay

    def _compute_mst_delaunay(self) -> list[Edge]:
        """Calculates the minimum spanning tree of a Delaunay triangulation.

        Returns:
            A list of the edges in the minimum spanning tree.
        """
        return _prim(self.delaunay)

    def _compute_delaunay(self):
        """Computes the Delaunay triangulation using the Guibas-Stolfi divide-and-conquer algorithm.

        Args:
            vertices: Vertices of the graph.

        Returns:
            A tuple consisting of the left edge, the right edge, the list of all edges (including symmetric), and a list of Delaunay edges (excluding symmetric).
        """
        left, right, bad_edges = _delaunay(self._vertices, self._edges, [])
        edges = list(set(self.edges) - set(bad_edges))
        delaunay_edges = []
        for e in edges:
            if not e.dual and e.org < e.dest:
                delaunay_edges.append(e)
        return left, right, edges, delaunay_edges

    def _compute_voronoi(self):
        """REDO DOCSTRING Computes the origin (org) and destination (dest) coordinates of the Voronoi edges, and the radius of the circumcircle of centered around the origin.

        The outer edges of the Voronoi diagram extend to infinity, which is treated as a single point.
        """
        return _voronoi(self.triangles, self.hull)

    def run(self):
        """Computes the graph's Delaunay triangulation, coordinates of the Voronoi edges, and the minimum spanning tree of the Delaunay triangulation."""
        self._left, self._right, self._edges, self._delaunay = self._compute_delaunay()
        self._voronoi = self._compute_voronoi()
        self._mst_delaunay = self._compute_mst_delaunay()


def _voronoi(triangles: list[list[Edge]], hull: list[Edge]) -> list[Edge]:
    """Docstring todo"""
    voronoi_edges = []
    for t in triangles:
        for e in t:
            vo = e.rot
            if e not in hull:
                vo.org, r_sym = circumcircle(e.sym)
                vo.sym.radius = r_sym
            else:
                vo.org = (float("inf"), float("inf"))

            vo.sym.org, r = circumcircle(e)
            vo.radius = r
            vo.sym.radius = r
            if vo.org < vo.dest:
                voronoi_edges.append(vo)
    return voronoi_edges


def _prim(graph: list[Edge]) -> list[Edge]:
    """Calculates the minimum spanning tree of a graph using Prim's algorith.

    Args:
        graph: Edges of a Delaunay triangulation or a Voronoi diagram.

    Returns:
        A list of the edges in the minimum spanning tree.
    """
    visited = {}
    mst = []
    heap = []

    first = graph[0]
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
    return mst


def _delaunay(s, edges, bad_edges):
    """Docstring to-do"""
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
    (ldo, ldi, _) = _delaunay(s[:mid], edges, bad_edges)
    (rdi, rdo, _) = _delaunay(s[mid:], edges, bad_edges)
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

        # caching
        basel_org = basel.org
        basel_dest = basel.dest
        basel_sym = basel.sym
        lvalid = valid(lcand, basel)

        if lvalid:
            while incircle(basel_dest, basel_org, lcand.dest, lcand.onext.dest):
                t = lcand.onext
                delete_quad_edge(lcand)
                bad_edges.extend([lcand, lcand.sym, lcand.rot, lcand.tor])
                lcand = t

        rcand = basel.oprev
        rvalid = valid(rcand, basel)

        if rvalid:
            while incircle(basel_dest, basel_org, rcand.dest, rcand.oprev.dest):
                t = rcand.oprev
                delete_quad_edge(rcand)
                bad_edges.extend([rcand, rcand.sym, rcand.rot, rcand.tor])
                rcand = t

        lcand_dest = lcand.dest
        rcand_dest = rcand.dest
        lvalid = valid(lcand, basel)
        rvalid = valid(rcand, basel)

        if not lvalid and not rvalid:
            break

        if not lvalid or (
            rvalid and incircle(lcand_dest, lcand.org, rcand.org, rcand_dest)
        ):
            basel = connect(rcand, basel_sym)
            edges.extend([basel, basel.sym, basel.rot, basel.tor])
        else:
            basel = connect(basel_sym, lcand.sym)
            edges.extend([basel, basel.sym, basel.rot, basel.tor])
    return (ldo, rdo, bad_edges)

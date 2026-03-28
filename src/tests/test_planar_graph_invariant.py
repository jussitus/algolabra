from math import isinf
from sympy import Matrix
import pytest
from utils.point_generation import points_circular
from planar_graph import PlanarGraph
from condition import incircle

N_SMALL = 100
N_MEDIUM = 1000
N_LARGE = 10000
POINTS_SMALL = points_circular(N_SMALL, N_SMALL // 2, N_SMALL // 2, 42)
POINTS_MEDIUM = points_circular(N_MEDIUM, N_MEDIUM // 2, N_MEDIUM // 2, 42)
POINTS_LARGE = points_circular(N_LARGE, N_LARGE // 2, N_LARGE // 2, 42)


@pytest.fixture
def graph_small() -> PlanarGraph:
    graph = PlanarGraph(POINTS_SMALL)
    graph.run()
    return graph


@pytest.fixture
def graph_medium() -> PlanarGraph:
    graph = PlanarGraph(POINTS_MEDIUM)
    graph.run()
    return graph


@pytest.fixture
def graph_large() -> PlanarGraph:
    graph = PlanarGraph(POINTS_LARGE)
    graph.run()
    return graph


def slow_incircle(a, b, c, d) -> bool:
    matrix = Matrix(
        [
            [a[0], a[1], (a[0]) ** 2 + (a[1]) ** 2, 1],
            [b[0], b[1], (b[0]) ** 2 + (b[1]) ** 2, 1],
            [c[0], c[1], (c[0]) ** 2 + (c[1]) ** 2, 1],
            [d[0], d[1], (d[0]) ** 2 + (d[1]) ** 2, 1],
        ]
    )
    det = matrix.det()
    return det > 0


def test_delaunay_condition_independent(graph_small):
    graph = graph_small
    for t in graph.triangles:
        triangle_vertices = [v.org for v in t]
        for v in graph.vertices:
            if v not in triangle_vertices:
                assert not incircle(
                    triangle_vertices[0], triangle_vertices[1], triangle_vertices[2], v
                )


def test_delaunay_condition_dependent(graph_medium):
    graph = graph_medium
    for t in graph.triangles:
        triangle_vertices = [v.org for v in t]
        for v in graph.vertices:
            if v not in triangle_vertices:
                assert not incircle(
                    triangle_vertices[0], triangle_vertices[1], triangle_vertices[2], v
                )


def test_delaunay_correct_number_of_edges(graph_large):
    k = len(graph_large.hull)
    n = len(graph_large.vertices)
    edges = 4 * (3 * n - 3 - k)
    assert len(graph_large.edges) == edges


def test_delaunay_correct_number_of_triangles(graph_large):
    k = len(graph_large.hull)
    n = len(graph_large.vertices)
    triangles = 2 * n - 2 - k
    assert len(graph_large.triangles) == triangles


def test_each_hull_edge_in_only_one_triangle(graph_large):
    graph = graph_large
    for e in graph.hull:
        count = 0
        for t in graph.triangles:
            if e in t:
                count += 1
        assert count == 1


def test_same_number_of_delaunay_and_voronoi_edges(graph_large):
    graph = graph_large
    assert len(graph.delaunay) == len(graph.voronoi)


def test_all_non_hull_voronoi_edges_have_finite_geometry(graph_large):
    graph = graph_large
    hull = set(graph.hull)
    for e in graph.edges:
        if e.dual and (e.rot not in hull and e.rot.sym not in hull):
            # split test?
            assert e.radius is not None
            assert e.radius > 0
            assert not isinf(e.org[0])
            assert not isinf(e.dest[0])


def test_all_hull_voronoi_edges_extend_to_infinity(graph_large):
    graph = graph_large
    hull = set(graph.hull)
    for e in hull:
        vo = e.rot
        assert isinf(vo.org[0]) or isinf(vo.dest[0])

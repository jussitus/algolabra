

"""
ideioita:
- incircle epätosi kaikille pisteille joka kolmiolle (determinantti sympylla? niin on eri kuin käytössä oleva incircle testi)
- käy läpi sivut ja varmista että kärkiä sama määrä kuin syötteessä
- jos len(delaunay.hull) = k niin kolmioita 2n - 2 - k ja sivuja 3n - 3 - k
- hull = sivut jotka kuuluvat vain yhteen kolmioon
- ...

"""
from sympy import Matrix
import pytest
from point_generation import points_circular
from delaunay import PlanarGraph
from tqdm import tqdm
N_SMALL = 5
N_LARGE = 5
POINTS_SMALL = points_circular(N_SMALL, N_SMALL // 2, N_SMALL // 2, 42)
POINTS_LARGE = points_circular(N_LARGE, N_LARGE // 2, N_LARGE // 2, 42)

@pytest.fixture
def graph_small() -> PlanarGraph:
    graph = PlanarGraph(POINTS_SMALL)
    graph.run()
    return graph

@pytest.fixture
def graph_large() -> PlanarGraph:
    graph = PlanarGraph(POINTS_LARGE)
    graph.run()
    return graph

def incircle(a,b,c,d) -> bool:
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


def test_delaunay_condition(graph_small):
    all_correct = True
    for t in graph_small.triangles:
        triangle_vertices = [v.org for v in t]
        correct = True
        for v in graph_small.vertices:
            if v not in triangle_vertices:
                correct = not incircle(triangle_vertices[0], triangle_vertices[1], triangle_vertices[2], v)
        all_correct = correct
    assert all_correct

def test_delaunay_correct_number_of_edges(graph_large):
    k = len(graph_large.hull)
    n = len(graph_large.vertices)
    edges = 4 * (3*n - 3 - k)
    assert len(graph_large.edges) == edges

def test_delaunay_correct_number_of_triangles(graph_large):
    k = len(graph_large.hull)
    n = len(graph_large.vertices)
    triangles = (2*n - 2 - k)
    assert len(graph_large.triangles) == triangles 
import pytest
from delaunay import PlanarGraph

point_lists = [[(0,0), (1,1)], [(0,0), (0,1), (1,0)]]

def test_constructor_vertices_are_sorted():
    g = PlanarGraph([(2, 2), (0,1), (0,0),(1,1)])
    assert g.vertices == [(0,0), (0,1), (1,1), (2,2)]

@pytest.mark.parametrize("points", point_lists)
def test_constructor_computed_attributes_are_empty(points):
    g = PlanarGraph(points)
    computed_empty = [g.edges, g.delaunay, g.voronoi, g.hull, g.triangles, g.mst_delaunay]
    for c in computed_empty:
        assert len(c) == 0
    computed_none = [g.left, g.right]
    for c in computed_none:
        assert c is None
@pytest.mark.parametrize("points", point_lists)
def test_constructor_input_points_and_vertices_have_same_length(points):
    g = PlanarGraph(points)
    assert len(points) == len(g.vertices)

# def test_one_triangle

# def test_degenerate_points_no_triangle

# def test_hull

# def test__delaunay_2_and_3_and_3_degenerate

# def test__voronoi

# def test_prim_V_minus_1



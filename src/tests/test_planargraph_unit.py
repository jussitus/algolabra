import pytest
from delaunay import PlanarGraph, _prim, _voronoi
from condition import ccw
from edge import connect, make_quad_edge, splice
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

def test_triangle_non_collinear():
    g = PlanarGraph([(0,0), (0,1), (1,0)])
    g._left, g._right, g._edges, g._delaunay = g._compute_delaunay()
    
    assert len(g.triangles) == 1
    t = g.triangles[0]
    assert len(t) == 3
    a, b, c = t[0].org, t[1].org, t[2].org
    assert ccw(a,b,c)

def test_triangle_with_collinear_vertices_has_no_triangle():
    g = PlanarGraph([(0,0), (1,0), (2,0)])
    g._left, g._right, g._edges, g._delaunay = g._compute_delaunay()
    
    assert len(g.triangles) == 0

def test_hull_two_vertices():
    g = PlanarGraph([(0,0), (0,1)])
    g._left, g._right, g._edges, g._delaunay = g._compute_delaunay()

    assert len(g.hull) == 2
    assert g.hull[0] is g.hull[1].sym

def test_hull_three_vertices():
    g = PlanarGraph([(0,0), (0,1), (1,0)])
    g._left, g._right, g._edges, g._delaunay = g._compute_delaunay()

    assert len(g.hull) == 3
    assert g.hull[0].lnext.lnext.lnext is g.hull[0]
    assert sorted(g.hull) == sorted(g.triangles[0])

def test__delaunay_one_vertex():
    g = PlanarGraph([(0,0)])
    with pytest.raises(ValueError) as excinfo:
        g._compute_delaunay()
    assert "Number of points must be at least 2" in str(excinfo.value)

def test__delaunay_two_vertices():
    g = PlanarGraph([(0,0), (0,1)])
    g._left, g._right, g._edges, g._delaunay = g._compute_delaunay()

    assert len(g.edges) == 4
    assert g.left is not None and g.right is not None
    assert g.left is g.right.sym
    assert len(g.delaunay) == 1
    assert g.left in g.delaunay
    assert g.right not in g.delaunay

def test__delaunay_three_vertices_non_collinear_case_1():
    g = PlanarGraph([(0,0), (1,0), (1,1)])
    g._left, g._right, g._edges, g._delaunay = g._compute_delaunay()

    assert len(g.edges) == 12
    assert g.left is not None and g.right is not None
    assert len(g.delaunay) == 3
    assert g.left in g.delaunay
    assert g.right not in g.delaunay
def test__delaunay_three_vertices_non_collinear_case_2():
    g = PlanarGraph([(0,0), (1,1), (1,0)])
    g._left, g._right, g._edges, g._delaunay = g._compute_delaunay()

    assert len(g.edges) == 12
    assert g.left is not None and g.right is not None
    assert len(g.delaunay) == 3
    assert g.left in g.delaunay
    assert g.right not in g.delaunay

def test__delaunay_three_vertices_collinear():
    g = PlanarGraph([(0,0), (0,1), (0,2)])
    g._left, g._right, g._edges, g._delaunay = g._compute_delaunay()

    assert len(g.edges) == 8
    assert g.left is not None and g.right is not None
    assert g.left is not g.right.sym
    assert len(g.delaunay) == 2
    assert g.left in g.delaunay
    assert g.right not in g.delaunay
    
def test__voronoi_three_vertices():
    g = PlanarGraph([(0,0), (1,0), (1,1)])
    e1 = make_quad_edge((0,0), (1,0))
    e2 = make_quad_edge((1,0), (1,1))
    splice(e1.sym, e2)
    e3 = connect(e2, e1)

    triangles = [(e1,e2,e3)]
    delaunay_edges = [e1,e2,e3]
    hull = [e1,e2,e3]  
    voronoi_edges = _voronoi(triangles, delaunay_edges, hull)
    for vo in voronoi_edges:
        assert vo.org == (float('inf'), float('inf'))
        assert vo.sym.org == (0.5, 0.5)

def test__prim_rectangle():
    g = PlanarGraph([(0,0), (1,0), (1,2), (0,2)])
    _, _, _, delaunay_edges = g._compute_delaunay()
    mst = _prim(delaunay_edges)
    assert len(mst) == 3
    total_length = 0
    for e in mst:
        total_length += e.length
    assert total_length == 4

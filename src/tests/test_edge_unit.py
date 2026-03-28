import pytest
from edge import Edge, make_quad_edge

def test_new_edge_component():
    e = Edge()
    assert e.onext == e
    assert not e.dual
    assert e.radius is None
    assert e.length == float("inf")

def test_new_quad_edge():
    origin = (0,1)
    destination = (1,1)
    e = make_quad_edge(origin, destination)

    assert e.org == origin
    assert e.dest == destination
    assert e.sym.org == destination
    assert e.sym.dest == origin

    assert e is e.sym.sym
    assert e.rot is e.tor.sym
    assert e is e.tor.rot
    assert e is e.rot.tor

    assert not e.dual
    assert not e.sym.dual
    assert e.rot.dual
    assert e.tor.dual

# def test_derived_operators

# def test_splice

# def test_connect

# def test_delete_quad_edge

# def test_triangle_ccw

# def test_triangle_cw

# def test_circumcircle
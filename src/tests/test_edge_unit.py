import pytest
from edge import Edge, connect, delete_quad_edge, make_quad_edge, splice


def test_constructor_edge():
    e = Edge()
    assert e.onext == e
    assert not e.dual
    assert e.radius is None
    assert e.length == float("inf")


def test_make_quad_edge():
    origin = (0, 1)
    destination = (1, 1)
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


def test_new_quad_edge_derived_operators():
    e = make_quad_edge((0, 0), (1, 1))
    assert e.lnext is e.sym
    assert e.rnext is e.sym
    assert e.dnext is e
    assert e.oprev is e
    assert e.rprev is e.sym


def test_splice():
    a = make_quad_edge((0, 0), (1, 0))
    b = make_quad_edge((0, 1), (1, 1))
    assert a is a.onext
    assert b is b.onext
    splice(a, b)
    assert a is not a.onext
    assert b is not b.onext
    assert a.onext is b
    assert b.onext is a


def test_connect():
    a = make_quad_edge((0, 0), (1, 0))
    b = make_quad_edge((0, 1), (1, 1))
    c = connect(a, b)
    assert c.org == a.dest
    assert c.dest == b.org
    assert a.lnext is c
    assert c.lnext is b
    assert b.lnext.lnext is c.sym
    assert b.lnext.lnext.lnext is a.sym


def test_delete_quad_edge():
    a = make_quad_edge((0, 0), (1, 0))
    b = make_quad_edge((0, 1), (1, 1))
    c = connect(a, b)
    delete_quad_edge(c)
    assert a.lnext is a.sym
    assert b.lnext.lnext is b


# def test_triangle_ccw

# def test_triangle_cw

# def test_circumcircle

from collections import deque
from edge import Edge
from graphics import EdgeDrawer
from labyrinth import Labyrinth
def dfs(start):
    q = deque()
    q.append(start)
    closed = {}
    res = []
    while len(q) > 0:
        p = q.popleft()
        res.append(p)
        ring = [p]
        current = p.onext
        while current is not p:
            ring.append(current)
            current = current.onext
        print(len(ring))
        for e in ring:
            if closed.get(e.sym.org) is not None:
                continue
            q.append(e.sym)
            closed[e.sym.org] = True
    return res

def test_same_edges():
    lab = Labyrinth(2, 1, 1, 1, 1, "square", 0)
    start = lab.rooms[0].corner_edge
    edges_dfs = dfs(start)
    edges_lab = []
    for rectangle in lab.rooms + lab.corridors:
        for edge in rectangle.edges:
            edges_lab.append(edge)
            edges_lab.append(edge.sym)
    edges = [(e.org,e.dest) for e in edges_dfs]
    edge_drawer = EdgeDrawer()
    edge_drawer.add_edges(edges, colors="black", linewidths=1.5)
    edge_drawer.show()


from collections import deque, Counter
from edge import Edge
from graphics import Drawer
from labyrinth import Labyrinth


def dfs(start):
    q = deque()
    q.append(start)
    res = set()
    while len(q) > 0:
        p = q.popleft()
        ring = [p]
        current = p.onext
        while current is not p:
            ring.append(current)
            current = current.onext
        for e in ring:
            if e.sym in res:
                continue
            q.append(e.sym)
            res.add(e.sym)
    return list(res)


def test_search_using_edge_connections_finds_everything():
    lab = Labyrinth(20, 1, 3, 5, 1, "square", 0)
    start = lab.rooms[0].corner_edge
    edges_dfs = dfs(start)
    edges_lab = []
    for rectangle in lab.rooms + lab.corridors:
        for edge in rectangle.edges:
            edges_lab.append(edge)
            edges_lab.append(edge.sym)
    edges_lab = list(set(edges_lab))
    assert Counter(edges_dfs) == Counter(edges_lab)


def test_hand_on_wall_gets_back_to_start():
    lab = Labyrinth(2, 1, 3, 5, 1, "square", 0.5)
    start = lab.rooms[0].corner_edge
    edges_dfs = dfs(start)
    k = len(edges_dfs)
    found = False
    current = start.rnext
    for i in range(k):
        if current is start:
            found = True
            break
        current = current.rnext
        print(i)
    assert found

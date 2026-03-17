from collections import deque
from edge import Edge


def bfs(e: Edge) -> list:
    def mark(e):
        e.data = True
        edges.append(e)

    q = deque()
    q.append(e)
    edges = []
    while len(q) > 0:
        e = q.popleft()
        current = e.lnext
        ring = [e, e.sym]
        if not current.data:
            ring.append(current)
        for k in ring:
            if k.data:
                continue
            mark(e)
            q.append(k)
    return edges

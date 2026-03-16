from collections import deque
from edge import Edge


def bfs(e: Edge) -> list:
    def mark(e, visited):
        visited.add(e)

    def checkVisited(e, visited):
        return e in visited

    q = deque()
    q.append(e)
    visited = set()

    while len(q) > 0:
        e = q.popleft()
        current = e.lnext
        ring = [e, e.sym]
        if not checkVisited(current, visited):
            ring.append(current)
        for k in ring:
            if checkVisited(k, visited):
                continue
            mark(e, visited)
            q.append(k)
    return list(visited)

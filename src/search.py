from collections import deque
from edge import Edge


def bfs_coords(e: Edge) -> list:
    def mark(e, visited):
        if e.org <= e.dest:
            visited.add((e.org, e.dest))
        else:
            visited.add((e.org, e.dest))

    def checkVisited(e, visited):
        if e.org <= e.dest:
            return (e.org, e.dest) in visited
        else:
            return (e.dest, e.org) in visited

    q = deque()
    q.append(e)
    visited = set()

    while len(q) > 0:
        e = q.popleft()
        for i in [e, e.lnext, e.lnext.lnext]:
            first = i
            current = i.onext
            ring = [i]
            while True:
                if first == current:
                    break
                ring.append(current)
                current = current.onext
            for k in ring:
                if checkVisited(k, visited):
                    continue
                q.append(k)
                mark(k, visited)
    return visited


def bfs_edges(e: Edge) -> list:
    def mark(e, visited):
        visited.add(e)

    def checkVisited(e, visited):
        return e in visited

    q = deque()
    q.append(e)
    visited = set()

    while len(q) > 0:
        e = q.popleft()
        for i in [e, e.lnext, e.lnext.lnext]:
            first = i
            current = i.onext
            ring = [i]
            while True:
                if first == current:
                    break
                ring.append(current)
                current = current.onext
            for k in ring:
                if checkVisited(k, visited):
                    continue
                q.append(k)
                mark(k, visited)
    return visited

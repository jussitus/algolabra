from edge import Edge, makeQuadEdge, splice, connect, deleteEdge
from condition import ccw, inCircle
a = makeQuadEdge(1,2)
b = makeQuadEdge(3,4)
print(a.onext.org, b.onext.org)
splice(a,b)
print(a.onext.org, b.onext.org)

a = (1,1)
b = (0,1)
c = (0,-1)
d = (1,1)
print(ccw(b,a,d))
print(inCircle(a,b,c,d))

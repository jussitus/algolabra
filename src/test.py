from edge import Edge, makeQuadEdge, splice, connect

a = makeQuadEdge(1,2)
b = makeQuadEdge(3,4)
c = connect(a,b)
print(a.org,a.dest)
print(c.org, c.dest)
print(b.org,b.dest)

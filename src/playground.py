from delaunay import Delaunay
from edge import circumcircles
import random
import networkx as nx
import matplotlib.pyplot as plt
from point_generation import points_random, points_circular, points_circular_unit
import matplotlib.pyplot as plt
from condition import ccw
from time import time
from math import log

n = 1000
s = points_circular(n, n, n, 1)
start = time()
d = Delaunay(s)
d.run()
end = time()
total = end - start
ratio = total / (n * log(n))
print(f"n = {n}, ratio = {ratio}, time = {total}")

print(f"edges: {len(d.edges)}")
print(f"vertices: {len(d.vertices)}")
print(f"delaunay lenth: {len(d.delaunay)}")
#for e in d.delaunay:
    #print(f"{e.org} -> {e.dest}")
# for e in d.delaunay:
#     print(e)


print(f"voronoi lenth: {len(d.voronoi)}")
print(f"hull len = {len(d.hull)}")
# start = time()
# d.run_voronoi()
# took = time() - start
# print(f"Calculated Voronoi, took: {took:.4f}")

print(f"mst size: {len(d.mst)}")
total = 0
for e in d.mst:
    total += e.length
print(f"mst length: {total}")
D = nx.Graph()
for e in d.mst:
    #print(e)
    a = e.org
    b = e.dest
    D.add_edge(a,b)
# for t in d.triangles:
#     for e in t:
#         a = e.org
#         b = e.dest
#         D.add_edge(a, b)
D = nx.Graph()
for e in d.mst:
    #print(e)
    a = e.org
    b = e.dest
    D.add_edge(a,b)
# for t in d.triangles:
#     for e in t:
#         a = e.org
#         b = e.dest
#         D.add_edge(a, b)

pos_d = {node: node for node in D.nodes()}

nx.draw(
    D,
    pos_d,
    with_labels=False,
    edge_color="black",
    node_color="black",
    node_size=10,
)
D_v = nx.Graph()
for e in d.delaunay:
    #print(e)
    a = e.org
    b = e.dest
    D_v.add_node(a)
    D_v.add_node(b)
pos_d_v = {node: node for node in D_v.nodes()}
nx.draw_networkx_nodes(
    D_v,
    pos_d_v,
    node_color="green",
    node_size=10,
)

# V = nx.Graph()
# for e in d.edges:
#     if e.dual and e.org is not None and e.dest is not None:
#         a = e.org
#         b = e.dest
#         V.add_edge(a, b)
# pos_v = {node: node for node in V.nodes()}
# nx.draw(V, pos_v, with_labels=False, edge_color="red", node_color="red", node_size=10)

#
ax = plt.gca()
ax.set_aspect("equal", adjustable="datalim")
# ccs = circumcircles(edges)
# for c in ccs:
#     circle = plt.Circle(c[0], c[1], color=("blue", 0.1), fill=False)
#     # ax.add_patch(circle)

plt.show()

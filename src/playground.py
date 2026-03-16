from delaunay import delaunay, voronoi
from edge import circumcircles
import random
import networkx as nx
import matplotlib.pyplot as plt
from search import bfs
from point_generation import points_spread, points_random, points_circular
import matplotlib.pyplot as plt
from condition import ccw
from time import time

s = points_circular(10000, 10000, 10000, 42)
print("Generated points.")
print(f"len(s) = {len(s)}")
# s = [(-1, 2), (0, 3), (2, 0), (4, 5)]
l, r = delaunay(s)
print("Triangulated.")
start = time()
edges = bfs(l)
took = time() - start
print(f"Traversed, took: {took}")
v = voronoi(l, edges)
edges_voronoi = bfs(v)
edges_v = []
for e in edges_voronoi:
    if e.org is not None and e.dest is not None:
        edges_v.append(e)
#
# print(f"len(edges) = {len(edges)}")
# D = nx.Graph()
# for e in edges:
#     a = e.org
#     b = e.dest
#     D.add_edge(a, b)
# print(f"len(D.nodes) = {len(D.nodes())}")

#
# pos_d = {node: node for node in D.nodes()}
#
# nx.draw(
#     D,
#     pos_d,
#     with_labels=False,
#     edge_color="black",
#     node_color="black",
#     node_size=10,
# )

V = nx.Graph()
for e in edges_v:
    a = e.org
    b = e.dest
    V.add_edge(a, b)
pos_v = {node: node for node in V.nodes()}
nx.draw(V, pos_v, with_labels=False, edge_color="red", node_color="red", node_size=10)

#
ax = plt.gca()
ax.set_aspect("equal", adjustable="datalim")
# ccs = circumcircles(edges)
# for c in ccs:
#     circle = plt.Circle(c[0], c[1], color=("blue", 0.1), fill=False)
#     # ax.add_patch(circle)

plt.show()

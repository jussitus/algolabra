from delaunay import Delaunay
from edge import circumcircles
import random
import networkx as nx
import matplotlib.pyplot as plt
from point_generation import points_random, points_circular
import matplotlib.pyplot as plt
from condition import ccw
from time import time

s = points_circular(1000, 2500, 2500, 2)
print("Generated points.")
print(f"len(s) = {len(s)}")
# s = [(-1, 2), (0, 3), (2, 0), (4, 5)]
start = time()
d = Delaunay(s)
l = d.run()
took = time() - start
print(f"Triangulated, took: {took}")
# start = time()
# edges = bfs(l)
# took = time() - start
# print(f"Traversed, took: {took}")
# v = voronoi(l, edges)
# edges_voronoi = bfs(v)
# edges_v = []
# for e in edges_voronoi:
#     if e.org is not None and e.dest is not None:
#         edges_v.append(e)

print(f"edges = {len(d.edges)}")
print(f"vertices= {len(d.vertices)}")
print("TRIANGLES:")
for t in d.triangles:
    print(f"{t[0]}, {t[1]}, {t[2]}")
D = nx.Graph()
for t in d.triangles:
    for e in t:
        a = e.org
        b = e.dest
        D.add_edge(a, b)


pos_d = {node: node for node in D.nodes()}

# nx.draw(
#     D,
#     pos_d,
#     with_labels=False,
#     edge_color="black",
#     node_color="black",
#     node_size=10,
# )
nx.draw_networkx_nodes(
    D,
    pos_d,
    node_color="black",
    node_size=10,
)

V = nx.Graph()
for e in d.edges:
    if e.dual and e.org is not None and e.dest is not None:
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

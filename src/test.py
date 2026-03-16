from delaunay import delaunay, voronoi
from edge import circumcircles
import random
import networkx as nx
import matplotlib.pyplot as plt
from search import bfs
from point_generation import points_spread, points_random, points_circular
import matplotlib.pyplot as plt
from condition import ccw

s = points_circular(50, 250, 250, -1)

# s = [(-1, 2), (0, 3), (2, 0), (4, 5)]
l, r = delaunay(s)
edges = bfs(l)
v = voronoi(l, edges)
edges_voronoi = bfs(v)
edges_v = []
for e in edges_voronoi:
    if e.org is not None and e.dest is not None:
        edges_v.append(e)
        print(e)

D = nx.Graph()
V = nx.Graph()
for e in edges:
    a = e.org
    b = e.dest
    D.add_edge(a, b)
for e in edges_v:
    a = e.org
    b = e.dest
    V.add_edge(a, b)

ccs = circumcircles(edges)
# for e in G.edges():
# print(e)
# for c in ccs:
#     print(c)
#     V.add_node(c[0])
pos_d = {node: node for node in D.nodes()}
pos_v = {node: node for node in V.nodes()}
# nx.draw(
#     D,
#     pos_d,
#     with_labels=False,
#     edge_color="black",
#     node_color="black",
#     node_size=10,
# )
nx.draw(V, pos_v, with_labels=False, edge_color="red", node_color="red", node_size=10)


ax = plt.gca()
ax.set_aspect("equal", adjustable="datalim")
for c in ccs:
    circle = plt.Circle(c[0], c[1], color=("blue", 0.1), fill=False)
    # ax.add_patch(circle)

plt.show()

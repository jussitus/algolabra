from delaunay import delaunay
import random
import networkx as nx
import matplotlib.pyplot as plt
from search import bfs_edges
from point_generation import points_spread, points_random

s = points_random(25, 250, 250, 42)


l, r = delaunay(s)
edges = bfs_edges(l)
# for e in edges:
#    print(e)
first = l
current = l.rprev
edges.remove(first)
while first != current:
    print(current)
    # edges.remove(current)
    # edges.remove(current.sym)
    current = current.rprev


G = nx.Graph()

for e in edges:
    a = e.org
    b = e.dest
    G.add_edge(a, b)

# for e in G.edges():
# print(e)
pos = {node: node for node in G.nodes()}
nx.draw(G, pos, with_labels=False, node_color="lightblue", node_size=5)
plt.show()

print(s)

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
from room_generation import Labyrinth


n = 25
lab = Labyrinth(n)
print(len(lab.rooms))
d = Delaunay(lab.room_centers)
d.run()

P = nx.Graph()
for e in d.mst_delaunay:
    P.add_edge(e.org, e.dest)
pos_p = {node: node for node in P.nodes()}
nx.draw(
    P,
    pos_p,
    with_labels=False,
    edge_color="red",
    node_color="red",
    node_size=0,
)


L = nx.Graph()
for room in lab.rooms:
    L.add_edge(room.corner_upper_left, room.corner_upper_right)
    L.add_edge(room.corner_lower_left, room.corner_lower_right)
    L.add_edge(room.corner_upper_left, room.corner_lower_left)
    L.add_edge(room.corner_upper_right, room.corner_lower_right)

pos_l = {node: node for node in L.nodes()}

nx.draw(
    L,
    pos_l,
    with_labels=False,
    edge_color="black",
    node_color="black",
    node_size=0,
)
ax = plt.gca()
ax.set_aspect("equal", adjustable="datalim")
plt.show()

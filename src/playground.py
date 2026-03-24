import logging

logging.basicConfig(level=logging.WARNING)

from log_utils import logger

logger.setLevel(logging.DEBUG)

from delaunay import PlanarGraph
import random
from point_generation import points_random, points_circular, points_circular_unit
from condition import ccw
from time import time
from math import floor, isinf
from labyrinth import Labyrinth

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# n = 10000
# points = points_circular(n, n, n, -1)
# #points = [(0, 0), (0, 1), (1, 0), (1, 1)]
# d = PlanarGraph(points)
# d.run()
# print(d)
# exit()
# fig, ax = plt.subplots()
# ax.axis("equal")
# edges_d = [(e.org, e.dest) for e in d.delaunay]
# edges_v = []
# for e in d.voronoi:
#     if not isinf(e.org[0]) and not isinf(e.dest[0]):
#         print(e)
#         edges_v.append((e.org, e.dest))
# l_d = LineCollection(edges_d, colors="black", linewidths=1.5)
# l_v = LineCollection(edges_v, colors="red", linewidths=1.5)
# ax.add_collection(l_d)
# ax.add_collection(l_v)
# ax.autoscale()
# plt.show()

# exit()

###
n = 500
lab = Labyrinth(n, 3)

rectangles = []
for room in lab.rooms:
    room_edges = [e.org for e in room.edges]
    room_edges.append(room.edges[-1].dest)
    rectangles.append(room_edges)

for room in lab.corridors:
    room_edges = [e.org for e in room.edges]
    room_edges.append(room.edges[-1].dest)
    rectangles.append(room_edges)

fig, ax = plt.subplots()
ax.axis("equal")
# p = PolyCollection(rectangles, facecolors='blue', edgecolors='blue')
l = LineCollection(rectangles, colors="black", linewidths=1.5)
# ax.add_collection(p)
ax.add_collection(l)


ax.autoscale()

plt.show()

from delaunay import PlanarGraph
import random
from point_generation import points_random, points_circular, points_circular_unit
from condition import ccw
from time import time
from math import floor
from labyrinth import Labyrinth
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection

n = 50
lab = Labyrinth(n, 1)

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
ax.axis('equal')
#p = PolyCollection(rectangles, facecolors='blue', edgecolors='blue')
l = LineCollection(rectangles, colors='black', linewidths=1.5)
#ax.add_collection(p)
ax.add_collection(l)


ax.autoscale()

plt.show()
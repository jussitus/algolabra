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

n = 250
lab = Labyrinth(n, 1)
# points = points_circular(n, n // 2, n // 2, 42)
# print(f"n={len(lab.rooms)}")
# d = PlanarGraph(lab.room_centers)
# d = PlanarGraph(points)
# d.run()
# exit()

rectangles = []
for room in lab.rooms:
    room_edges = [e.org for e in room.edges]
    room_edges.append(room.edges[-1].dest)
    rectangles.append(room_edges)

for room in lab.corridors:
    room_edges = [e.org for e in room.edges]
    room_edges.append(room.edges[-1].dest)
    rectangles.append(room_edges)



# counts = Counter(tuple(sorted(x)) for x in edges)
# edges = [x for x in edges if counts[tuple(sorted(x))] == 1]
# print(edges[0])
# vertices = [item for edge in edges for item in edge]
# vertices = list(set(vertices))

fig, ax = plt.subplots()
ax.axis('equal')
p = PolyCollection(rectangles, facecolors='blue', edgecolors='blue')
l = LineCollection(rectangles, colors='black', linewidths=1.5)
#ax.add_collection(p)
ax.add_collection(l)


ax.autoscale()

plt.show()
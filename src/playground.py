from delaunay import PlanarGraph
import random
from point_generation import points_random, points_circular, points_circular_unit
from condition import ccw
from time import time
from math import floor
from labyrinth2 import Labyrinth
from PIL import Image, ImageDraw, ImageOps

n = 10
lab = Labyrinth(n)
# points = points_circular(n, n // 2, n // 2, 42)
print(f"n={len(lab.rooms)}")
d = PlanarGraph(lab.room_centers)
# d = PlanarGraph(points)
d.run()
# exit()
extrema = d.extreme_vertices()
max_width = len(lab.room_squares[0])
max_height = len(lab.room_squares)
print(max_width, max_height)
canvas_width = 2048
canvas_height = 2048
print()
padding = floor(0.1 * max_width)
bg = "black"
fg = "white"

im = Image.new(
    "RGB",
    (int(canvas_width),int(canvas_width)),
    color=bg,
)


draw = ImageDraw.Draw(im)
for room in lab.rooms:
    for e in room.edges:
        org = tuple(map(lambda x: x, e.org))
        dest = tuple(map(lambda x: x, e.dest))
        draw.line((org, dest), fill="red", width=1)


# for room in lab.rooms:
#     p1 = room.corner_upper_left
#     p2 = room.corner_lower_right
#     p1_x = p1[0]
#     p1_y = p1[1]
#     p2_x = p2[0]
#     p2_y = p2[1]
#     draw.rectangle([p1_x, p1_y, p2_x, p2_y], fill=fg, outline=None)
# corridors = [
#     (x, y)
#     for y, col in enumerate(lab.corridor_squares)
#     for x, cor in enumerate(col)
#     if cor
# ]
# for square in corridors:
#     p1 = square
#     p2 = (square[0], square[1])
#     p1_x = p1[0]
#     p1_y = p1[1]
#     p2_x = p2[0]
#     p2_y = p2[1]
#     draw.rectangle(
#         [p1_x, p1_y, p2_x, p2_y], fill="blue", outline=None
#     )


im = ImageOps.expand(im, border=padding, fill=bg)
im = im.resize((canvas_width, canvas_height), Image.Resampling.NEAREST)


im.show()

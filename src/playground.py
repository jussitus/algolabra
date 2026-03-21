from delaunay import Delaunay
import random
from point_generation import points_random, points_circular, points_circular_unit
from condition import ccw
from time import time
from math import floor
from room_generation import Labyrinth
from PIL import Image, ImageDraw, ImageOps

n = 100
lab = Labyrinth(n)
#points = points_circular(n, 10000, 10000, 42)
print(f"n={len(lab.rooms)}")
d = Delaunay(lab.room_centers)
#d = Delaunay(points)
d.run()
#exit()
extrema = d.extreme_vertices()
max_width = extrema["max_x"][0] + lab.max_width
max_height = extrema["max_y"][1] + lab.max_height
anti_alias = 1
canvas_width = 2048
canvas_height = 2048
scale =  anti_alias * canvas_width / max_height
padding = floor(0.1 * canvas_width * anti_alias)
bg = "black"
fg = "white"

im = Image.new('RGB', (floor(anti_alias * canvas_width), floor(anti_alias * canvas_height)), color=bg)


draw = ImageDraw.Draw(im)
for e in d.delaunay:
    if e.length == float('inf'):
        continue
    org = tuple(map(lambda x: x*scale, e.org))
    dest = tuple(map(lambda x: x*scale, e.dest))
    draw.line((org,dest), fill='red', width=canvas_width // 1000)



for room in lab.rooms:
    p1 = room.corner_upper_left
    p2 = room.corner_lower_right
    p1_x = p1[0]*scale
    p1_y = p1[1]*scale
    p2_x = p2[0]*scale
    p2_y = p2[1]*scale
    draw.rectangle([p1_x, p1_y, p2_x, p2_y], fill=fg, outline=None)
corridors = [(x,y) for y, col in enumerate(lab.corridor_squares) for x, cor in enumerate(col) if cor]
for square in corridors:
    p1 = square
    p2 = (square[0] + 1, square[1] + 1)
    p1_x = p1[0]*scale
    p1_y = p1[1]*scale
    p2_x = p2[0]*scale
    p2_y = p2[1]*scale
    draw.rectangle([p1_x, p1_y, p2_x, p2_y], fill="blue", outline=None, width=canvas_width // 50)


im = ImageOps.expand(im, border=padding, fill=bg)
#im = im.resize((canvas_width, canvas_height), Image.Resampling.LANCZOS)


im.show()
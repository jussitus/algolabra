from random import randint, seed
from math import sqrt, floor
import heapq as hq
from tqdm import tqdm
from delaunay import PlanarGraph
from edge import Edge, make_quad_edge, splice
from point import Point

# WIP

class Room:
    def __init__(self, corner, width, height):
        self.width = width
        self.height = height
        self.corner = corner
        self.corner_edge: Edge = None # type: ignore
        self.edges = []
        self.connected = False

    def create_room(self):
        def add_side(edges, current, length, displacement):
            for _ in range(length):
                next_org = current.dest
                next_dest = (next_org[0] + displacement[0], next_org[1] + displacement[1])
                next = make_quad_edge(next_org, next_dest)
                splice(current.sym, next)
                current = next
                edges.append(current)
            return current
        edges = []
        corner_edge = make_quad_edge(self.corner, (self.corner[0] + 1, self.corner[1]))
        edges.append(corner_edge)
        top = add_side(edges, corner_edge, self.width - 1, (1,0))
        right = add_side(edges, top, self.height, (0,1))
        bottom = add_side(edges, right, self.width, (-1,0))
        left = add_side(edges, bottom, self.height, (0,-1))
        splice(left.sym, corner_edge)
        self.edges = edges
        self.corner_edge = corner_edge

class Labyrinth:
    def __init__(self, n_rooms):
        self.n_rooms = n_rooms
        self.max_width = 5  # max(5, floor(sqrt(max_rooms)))
        self.max_height = 5  # max(5, floor(sqrt(max_rooms)))
        self.min_width = max(2, self.max_width // 3)
        self.min_height = max(2, self.max_height // 3)
        self.gap = 1
        self.sparsity = 0.5 * (self.max_width) / n_rooms
        self.max_tries = 100
        self.room_squares = [[None] * (floor(self.n_rooms * self.max_width * self.sparsity)) for _ in range(floor(self.n_rooms * self.max_height * self.sparsity))]
        self.corridor_squares = [
            [None] * len(self.room_squares) for _ in range(len(self.room_squares))
        ]
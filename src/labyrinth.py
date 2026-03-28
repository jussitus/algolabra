from enum import Enum, auto
import random
from math import sqrt, floor
import heapq as hq
from typing import Self
from delaunay import PlanarGraph
from edge import Edge, make_quad_edge, splice, delete_quad_edge
from point import Point, PointInt


class Rectangle:
    def __init__(self, corner: PointInt, width: int = 1, height: int = 1):
        self.width: int = width
        self.height: int = height
        self.corner: PointInt = corner
        self.center: PointInt = (corner[0] + width // 2, corner[1] + height // 2)
        self.edges: list[Edge]
        self.corner_edge: Edge
        self.edges, self.corner_edge = self.create()

    def create(self) -> tuple[list[Edge], Edge]:
        edges: list[Edge] = []
        corner_edge = make_quad_edge(self.corner, (self.corner[0] + 1, self.corner[1]))
        edges.append(corner_edge)
        top = self.add_side(edges, corner_edge, self.width - 1, (1, 0))
        right = self.add_side(edges, top, self.height, (0, 1))
        bottom = self.add_side(edges, right, self.width, (-1, 0))
        left = self.add_side(edges, bottom, self.height, (0, -1))
        splice(left.sym, corner_edge)
        return edges, corner_edge

    def add_side(
        self, edges: list[Edge], current: Edge, length: int, displacement: Point
    ) -> Edge:
        for _ in range(length):
            next_org = current.dest
            next_dest = (
                next_org[0] + displacement[0],
                next_org[1] + displacement[1],
            )
            next = make_quad_edge(next_org, next_dest)
            splice(current.sym, next)
            current = next
            edges.append(current)
        return current


class Room(Rectangle):
    def __init__(self, *args):
        super().__init__(*args)


class Corridor(Rectangle):
    def __init__(self, *args):
        super().__init__(*args)


class Labyrinth:
    def __init__(self, num_rooms: int, seed: int, max_dim: int, min_dim: int):
        self.num_rooms: int = num_rooms
        self.seed: int = seed
        self.max_dim: int = max_dim
        self.min_dim: int = min_dim
        self.gap: int = 5
        self.rooms: list[Room]
        self.room_squares: list[list[Room | None]]
        self.room_centers: list[PointInt]
        self.rooms, self.room_squares, self.room_centers = self._generate_rooms()
        self.room_edge_index = self._index_room_edges()
        self.corridor_edge_index = {}
        self.corridor_squares: list[list[Corridor | None]] = [
            [None] * len(self.room_squares) for _ in range(len(self.room_squares))
        ]

        self.corridors: list[Corridor] = self._create_corridors()

    def _generate_rooms(
        self,
    ) -> tuple[
        list[Room],
        list[list[Room | None]],
        list[PointInt],
    ]:
        room_generator = RoomGenerator(
            self.num_rooms, self.min_dim, self.max_dim, self.gap, "square", self.seed
        )
        return room_generator.run()

    def _create_corridors(self):
        connections = self._connect_rooms(self.room_centers)
        corridors: list[Corridor] = []
        path_finder = PathFinder(self)
        for edge in connections:
            path: Path | None = path_finder.find_path(edge.org, edge.dest)
            current = path
            while current is not None:
                if self.get_corridor_of_square(current.current) is None:  
                    corridor = Corridor(current.current)
                    self.corridor_squares[current.current[1]][
                        current.current[0]
                    ] = corridor
                    self._index_corridor_edges(corridor)
                    self._link_corridor(corridor)
                    if self.get_room_of_square(current.current) is None:
                        corridors.append(corridor)
                current = current.path
        return corridors

    def _link_corridor(self, corridor):
        edges = []
#WRONG
        for e in corridor.edges:
            if self.get_room_of_square(e.org) is not None or self.get_corridor_of_square(e.org) is not None:
                re = self.room_edge_index.get((e.org,e.dest))
                if re is None:
                    re = self.corridor_edge_index.get((e.org, e.dest))
                if re is not None:
                    splice(e, re)
                    splice(e.sym, re.sym)
                    re.data = "door"
                    re.sym.data = "door"
                    edges.append(re)
                else:
                    edges.append(e)
            else:
                edges.append(e)
        corridor.edges = edges
    def get_room_of_square(self, square: PointInt):
        return self.room_squares[square[1]][square[0]]

    def get_corridor_of_square(self, square: PointInt):
        return self.corridor_squares[square[1]][square[0]]

    def _connect_rooms(self, room_centers: list[PointInt]) -> list[Edge]:
        d = PlanarGraph(room_centers)
        d.run()
        connections: list[Edge] = d.mst_delaunay
        return connections

    def _index_room_edges(self):
        index = {}
        for room in self.rooms:
            for e in room.edges:
                index[(e.org, e.dest)] = e
                index[(e.dest, e.org)] = e.sym
        return index
    
    def _index_corridor_edges(self,corridor):
        for e in corridor.edges:
            self.corridor_edge_index[(e.org, e.dest)] = e
            self.corridor_edge_index[(e.dest, e.org)] = e.sym
class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


class Path:
    def __init__(
        self,
        f_length: float,
        g_length: float,
        current: PointInt,
        direction: Direction | None,
        path: Path | None = None,
    ):
        self.f_length: float = f_length
        self.g_length: float = g_length
        self.current: PointInt = current
        self.direction: Direction | None = direction
        self.path: Path | None = path

    def __lt__(self, other: Self) -> bool:
        return self.f_length < other.f_length


class PathFinder:
    def __init__(self, labyrinth: Labyrinth):
        self.labyrinth: Labyrinth = labyrinth

    def find_path(self, start: PointInt, end: PointInt) -> Path | None:
        first = Path(self._heuristic(start, end), 0, start, None, None)
        size = len(self.labyrinth.corridor_squares)
        closed_list = [[False] * size for _ in range(size)]
        open_list = [first]
        while len(open_list) > 0:
            current = hq.heappop(open_list)
            if self._found(current, end):
                return current
            self._expand(open_list, closed_list, current, end)
        return None

    def _close(self, closed_list: list[list[bool]], square: PointInt):
        closed_list[square[1]][square[0]] = True

    def _closed(self, closed_list: list[list[bool]], square: PointInt):
        return closed_list[square[1]][square[0]]

    def _expand(
        self,
        open_list: list[Path],
        closed_list: list[list[bool]],
        current_path: Path,
        end: PointInt,
    ):
        if self._closed(closed_list, current_path.current):
            return
        self._close(closed_list, current_path.current)
        neighbors = self._neighbors(current_path.current)
        for neighbor, direction in neighbors:
            if self._closed(closed_list, neighbor):
                continue
            weight = 0.5 if self._is_corridor(neighbor) else 1
            g = current_path.g_length + weight
            h = self._heuristic(neighbor, end)
            path = Path(g + h, g, neighbor, direction, current_path)
            hq.heappush(open_list, path)

    def _is_corridor(self, square):
        return self.labyrinth.get_corridor_of_square(square) is not None

    def _is_room(self, square):
        return self.labyrinth.get_room_of_square(square) is not None

    def _found(self, path: Path, end: PointInt):
        room = self.labyrinth.get_room_of_square(path.current)
        return room is not None and room.center == end

    def _heuristic(self, a: PointInt, b: PointInt):
        # return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        # return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    def _neighbors(self, square: PointInt) -> list[tuple[PointInt, Direction]]:
        squares: list[tuple[PointInt, Direction]] = []
        if square[1] + 1 < len(self.labyrinth.room_squares):
            north = (square[0], square[1] + 1)
            squares.append((north, Direction.NORTH))
        if square[1] > 0 and square[1] - 1 < len(self.labyrinth.room_squares):
            south = (square[0], square[1] - 1)
            squares.append((south, Direction.SOUTH))
        if square[0] > 0 and square[0] - 1 < len(self.labyrinth.room_squares[0]):
            west = (square[0] - 1, square[1])
            squares.append((west, Direction.WEST))
        if square[0] + 1 < len(self.labyrinth.room_squares[0]):
            east = (square[0] + 1, square[1])
            squares.append((east, Direction.EAST))
        return squares


class RoomGenerator:
    def __init__(self, num_rooms, min_dim, max_dim, gap, shape, seed):
        self.num_rooms = num_rooms
        self.min_dim = min_dim
        self.max_dim = max_dim
        self.gap = gap
        self.shape = shape
        self.seed = seed

        self.size = max_dim
        self.max_tries = 1000

    def _generate_rooms(self):
        size = floor(self.size)
        rooms: list[Room] = []
        room_squares: list[list[Room | None]] = [[None] * (size) for _ in range(size)]
        room_centers: list[PointInt] = []
        occupied: list[list[bool]] = [[False] * (size) for _ in range(size)]
        tries = 0
        if self.seed != -1:
            random.seed(self.seed)
        while len(rooms) < self.num_rooms:
            if tries == self.max_tries:
                break
            corner = self._generate_point(size)
            width = random.randint(self.min_dim, self.max_dim)
            height = random.randint(self.min_dim, self.max_dim)
            if self._invalid_room(corner, size, width, height):
                tries += 1
                continue
            valid_room = self._room_fits(occupied, corner, width, height)
            if not valid_room:
                tries += 1
                continue
            tries = 0
            room = self._create_and_occupy_room(
                occupied, room_squares, size, corner, width, height
            )
            rooms.append(room)
            room_centers.append(room.center)
        return rooms, room_squares, room_centers

    def _generate_point(self, size):
        max_pos = size - self.max_dim
        if self.shape == "circle":
            return point_in_circle(max_pos)
        if self.shape == "square":
            return point_in_square(max_pos)
        else:
            raise ValueError("Bad shape")

    def _create_and_occupy_room(
        self, occupied, room_squares, size, corner, width, height
    ):
        room = Room(corner, width, height)
        for w in range(-self.gap, width + self.gap):
            if corner[0] + w >= size:
                break
            for h in range(-self.gap, height + self.gap):
                if corner[1] + h >= size:
                    break
                occupied[corner[1] + h][corner[0] + w] = True
                if w >= 0 and h >= 0 and w < width and h < height:
                    room_squares[corner[1] + h][corner[0] + w] = room
        return room

    def _room_fits(self, occupied, corner, width, height):
        for w in range(-self.gap, width):
            for h in range(-self.gap, height):
                if occupied[corner[1] + h][corner[0] + w]:
                    return False
        return True

    def _invalid_room(self, corner, size, width, height):
        return (
            corner[0] + width + self.gap > size
            or corner[1] + height + self.gap > size
            or corner[0] - self.gap < 0
            or corner[1] - self.gap < 0
        )

    def run(self):
        while True:
            rooms, room_squares, room_centers = self._generate_rooms()
            if len(rooms) == self.num_rooms:
                break
            self.size *= 1.1
        return rooms, room_squares, room_centers


def point_in_circle(max_pos: int):
    mid_x = max_pos // 2
    mid_y = max_pos // 2
    while True:
        x = random.randint(0, max_pos)
        y = random.randint(0, max_pos)
        if sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2) <= max(mid_x, mid_y):
            break
    return (x, y)


def point_in_square(max_pos: int):
    x = random.randint(0, max_pos)
    y = random.randint(0, max_pos)
    return (x, y)

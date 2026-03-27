from modulefinder import packagePathMap
from pickletools import int4
from posixpath import dirname
import random
from math import sqrt, floor
import heapq as hq
from typing import Self
from delaunay import PlanarGraph
from edge import Edge, make_quad_edge, splice
from point import Point, PointInt

# WIP


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
        self.gap: int = 1
        self.modifier: float = 1.1
        self.max_tries: int = 1000
        self.rooms: list[Room]
        self.room_squares: list[list[Room | None]]
        self.room_centers: list[PointInt]
        self.rooms, self.room_squares, self.room_centers = self.generate_rooms()
        self.corridor_squares: list[list[Corridor | None]] = [
            [None] * len(self.room_squares) for _ in range(len(self.room_squares))
        ]

        self.corridors: list[Corridor] = self.create_corridors()

    def generate_rooms(
        self,
    ) -> tuple[list[Room], list[list[Room | None]], list[PointInt]]:
        rooms: list[Room] = []
        room_centers: list[PointInt] = []
        total: int = floor(self.max_dim * self.modifier)
        occupied: list[list[bool]] = [[False] * (total) for _ in range(total)]
        room_squares: list[list[Room | None]] = [[None] * (total) for _ in range(total)]
        tries = 0
        if self.seed != -1:
            random.seed(self.seed)
        while len(rooms) < self.num_rooms:
            if tries == self.max_tries:
                # print(f"Could not fit any more rooms in {self.max_tries} tries for total={total}. Trying more sparse layout...")
                self.modifier *= 1.1
                return self.generate_rooms()
            valid = True
            corner = point_in_circle(total - self.max_dim)
            width = random.randint(self.min_dim, self.max_dim)
            height = random.randint(self.min_dim, self.max_dim)
            if (
                corner[0] + width + self.gap > len(room_squares[0])
                or corner[1] + height + self.gap > len(room_squares)
                or corner[0] - self.gap < 0
                or corner[1] - self.gap < 0
            ):
                tries += 1
                continue
            for w in range(-self.gap, width):
                for h in range(-self.gap, height):
                    if occupied[corner[1] + h][corner[0] + w]:
                        valid = False
                        break
            if not valid:
                tries += 1
                continue
            tries = 0
            # print(f"creating room {n}: corner={corner}, width={width}, height={height}")
            room = Room(corner, width, height)
            for w in range(-self.gap, width + self.gap):
                if corner[0] + w >= total:
                    break
                for h in range(-self.gap, height + self.gap):
                    if corner[1] + h >= total:
                        break
                    occupied[corner[1] + h][corner[0] + w] = True
                    if w >= 0 and h >= 0 and w < width and h < height:
                        room_squares[corner[1] + h][corner[0] + w] = room  # type: ignore
            rooms.append(room)
            room_centers.append(room.center)
        return rooms, room_squares, room_centers

    def create_corridors(self):
        connections = self.connect_rooms(self.room_centers)
        corridors: list[Corridor] = []
        path_finder = PathFinder(self)
        for edge in connections:
            path: Path | None = path_finder.find_path(edge.org, edge.dest)
            current = path
            while current is not None:
                # todo: add corridor room connect logic to Rectangle
                if self.get_room_of_square(current.current) is None:
                    if self.get_corridor_of_square(current.current) is None:
                        corridor = Corridor(current.current)
                        self.corridor_squares[current.current[1]][
                            current.current[0]
                        ] = corridor
                        corridors.append(corridor)
                current = current.path
        return corridors

    def get_room_of_square(self, square: PointInt):
        return self.room_squares[square[1]][square[0]]

    def get_corridor_of_square(self, square: PointInt):
        return self.corridor_squares[square[1]][square[0]]

    def connect_rooms(self, room_centers: list[PointInt]) -> list[Edge]:
        d = PlanarGraph(room_centers)
        d.run()
        connections: list[Edge] = d.mst_delaunay
        return connections


class Path:
    def __init__(
        self,
        f_length: float,
        g_length: float,
        current: PointInt,
        path: Path | None = None,
    ):
        self.f_length: float = f_length
        self.g_length: float = g_length
        self.current: PointInt = current
        self.path: Path | None = path

    def __lt__(self, other: Self) -> bool:
        return self.f_length < other.f_length


class PathFinder:
    def __init__(self, labyrinth: Labyrinth):
        self.labyrinth: Labyrinth = labyrinth
    

    def find_path(self, start: PointInt, end: PointInt) -> Path | None:
        first = Path(self._heuristic(start, end), 0, start, None)
        size = len(self.labyrinth.corridor_squares)
        closed_list = [[False]*size for _ in range(size)]
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

    def _expand(self, open_list: list[Path], closed_list: list[list[bool]], current_path: Path, end: PointInt):
        if self._closed(closed_list, current_path.current):
            return
        self._close(closed_list, current_path.current)
        neighbors = self._neighbors(current_path.current)
        for neighbor in neighbors:
            if self._closed(closed_list, neighbor):
                continue
            weight = 0.5 if self._is_corridor(neighbor) else 1
            g = current_path.g_length + weight
            h = self._heuristic(neighbor, end)
            path = Path(g+h, g, neighbor, current_path)
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
        

    def _neighbors(self, square: PointInt) -> list[PointInt]:
        squares: list[PointInt] = []
        if square[1] + 1 < len(self.labyrinth.room_squares):
            up = (square[0], square[1] + 1)
            squares.append(up)
        if square[1] > 0 and square[1] - 1 < len(self.labyrinth.room_squares):
            down = (square[0], square[1] - 1)
            squares.append(down)
        if square[0] > 0 and square[0] - 1 < len(self.labyrinth.room_squares[0]):
            left = (square[0] - 1, square[1])
            squares.append(left)
        if square[0] + 1 < len(self.labyrinth.room_squares[0]):
            right = (square[0] + 1, square[1])
            squares.append(right)
        return squares


def point_in_circle(width: int):
    mid_x = width // 2
    mid_y = width // 2
    while True:
        x = random.randint(0, width)
        y = random.randint(0, width)
        if sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2) <= max(mid_x, mid_y):
            point = (x, y)
            break
    return point

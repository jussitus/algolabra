import logging
from enum import Enum, auto
import random
from math import sqrt, floor
import heapq as hq
from typing import Self
from planar_graph import PlanarGraph
from edge import Edge, make_quad_edge, splice, delete_quad_edge
from point import PointInt, Point
from utils.log_utils import timer


class Rectangle:
    """Class representing a rectangle in a grid.

    Attributes:
        `width`: Width of the rectangle.
        'height': Height of the rectangle.
        'corner': Coordinates of the top-left corner of the rectangle.
        'edges': List of unit edges that make up the rectangle.
        'corner_edge': Edge corresponding to `self.corner`.
    """

    def __init__(self, corner: PointInt, width: int = 1, height: int = 1):
        """Initializes the rectangle.

        Args:
            `corner`: coordinates of the top-left corner
            'width': width of the rectangle
            'height': height of the rectangle
        """
        self.width: int = width
        self.height: int = height
        self.corner: PointInt = corner
        self.center: PointInt = (corner[0] + width // 2, corner[1] + height // 2)
        self.edges: list[Edge]
        self.corner_edge: Edge
        self.edges, self.corner_edge = self.create()

    def create(self) -> tuple[list[Edge], Edge]:
        """Creates and connects the edges of the rectangle.

        The edges are unit edges with length of 1.

        Returns:
            a list of rectangle unit edges

        """
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
        self, edges: list[Edge], current_edge: Edge, length: int, displacement: PointInt
    ) -> Edge:
        """Adds unit edges of one side of the rectangle.

        Args:
            `edges`: list of current edges
            `current_edge`: last edge of the previous side
            `length': length of the side
            `displacement`: direction of the side

        Returns:
            the last edge of the side

        """
        for _ in range(length):
            next_org = current_edge.dest
            next_dest = (
                next_org[0] + displacement[0],
                next_org[1] + displacement[1],
            )
            next_edge = make_quad_edge(next_org, next_dest)
            splice(current_edge.sym, next_edge)
            current_edge = next_edge
            edges.append(current_edge)
        return current_edge


class Room(Rectangle):
    """Subclass of `Rectangle`, representing a room."""

    def __init__(self, *args):
        super().__init__(*args)


class Corridor(Rectangle):
    """Subclass of `Rectangle`, representing a corridor square."""

    def __init__(self, *args):
        super().__init__(*args)


class Labyrinth:
    """"
    Class representing a labyrinth.

    Labyrinth is made up of rooms and corridors between rooms. The connections between rooms are calculated by computing the Delaunay triangulation of the room centers on a plane and then taking the edges of the minimum spanning tree. 
    
    Attributes:
        `num_rooms`: number of rooms in the labyrinth
        `seed`: random seed used to generate rooms
        `max_dim`: maximum dimension of a room
        `min_dim`: minimum dimension of a room
        `gap`: minimum amount of squares between rooms
        `shape`: shape of the labyrinth (square or circular)
        `rooms`: list of rooms
        `corridors`: list of corridor squares
        `squares`: index of squares in the labyrinth
        `room_centers`: list of room centers
        `edges`: index of edges in the labyrinth
    """
    def __init__(self, num_rooms: int, seed: int, max_dim: int, min_dim: int, gap: int, shape: str):
        """Instantiates the labyrinth.
        
        Args:
            `num_rooms`: number of rooms in the labyrinth
            `seed`: random seed used to generate rooms
            `max_dim`: maximum dimension of a room
            `min_dim`: minimum dimension of a room
            `gap`: minimum amount of squares between rooms
            `shape`: shape of the labyrinth (square or circular)
        """
        self.num_rooms: int = num_rooms
        self.seed: int = seed
        self.max_dim: int = max(max_dim, 1)
        self.min_dim: int = min(min_dim, self.max_dim)
        self.gap: int = gap
        self.shape: str = shape
        self.rooms: list[Room]
        self.squares: list[list[Rectangle | None]]
        self.room_centers: list[PointInt]
        self.rooms, self.squares, self.room_centers = self._generate_rooms()
        self.edges: dict[tuple[Point, Point], Edge] = self._index_room_edges()
        self.corridors: list[Corridor] = self._create_corridors()

    @timer(level=logging.DEBUG)
    def _generate_rooms(
        self,
    ) -> tuple[
        list[Room],
        list[list[Rectangle | None]],
        list[PointInt],
    ]:
        room_generator = RoomGenerator(
            self.num_rooms, self.min_dim, self.max_dim, self.gap, self.shape, self.seed
        )
        return room_generator.run()

    def _create_corridors(self) -> list[Corridor]:
        """
        Creates corridors.

        First connections between rooms are obtained from the minimum spanning tree. Then a path in the grid is found for each connection using A*.

        Returns:
            a list of `Corridor` squares
        """
        connections = self._connect_rooms(self.room_centers)
        corridors: list[Corridor] = []
        path_finder = PathFinder(self)
        for edge in connections:
            path: Path | None = path_finder.find_path(edge.org, edge.dest)  # pyright: ignore[reportArgumentType]
            current = path
            while current is not None:
                if self._get_square(current.current) is None:
                    corridor = Corridor(current.current)
                    self.squares[current.current[1]][current.current[0]] = corridor
                    self._link_corridor(corridor)
                    self._index_corridor_edges(corridor)
                    corridors.append(corridor)
                current = current.path
        return corridors

    def _link_corridor(self, corridor: Corridor):
        """Links edges of a corridor square with existing edges.

        Existing edges are preferred and any corridor edge sharing space is replaced with the existing one, after linking.
        """
        edges: list[Edge] = []
        for e in corridor.edges:
            re = self.edges.get((e.org, e.dest))
            if re is not None:  # type: ignore
                splice(e, re)
                splice(e.sym, re.sym)
                delete_quad_edge(e)
                re.data = "shared"
                re.sym.data = "shared"
                edges.append(re)
            else:
                edges.append(e)
        corridor.edges = edges

    def _get_square(self, square: PointInt) -> Rectangle | None:
        """Returns the square of the coordinate."""
        return self.squares[square[1]][square[0]]

    def _connect_rooms(self, room_centers: list[PointInt]) -> list[Edge]:
        """Computes the Delaunay triangulation of the room center points and the minimum spanning tree of the triangulation.
        
        Returns:
            the minimum spanning tree of the triangulation, representing connections in the labyrinth"""
        d = PlanarGraph(room_centers)
        d.run()
        connections: list[Edge] = d.mst_delaunay
        return connections

    def _index_room_edges(self) -> dict[tuple[Point, Point], Edge]:
        """Indexes the edges of all rooms, for lookup of existing edges.
        
        Returns:
            a dict of coordinate pairs and edges
        """
        index: dict[tuple[Point, Point], Edge] = {}
        for room in self.rooms:
            for e in room.edges:
                index[(e.org, e.dest)] = e
                index[(e.dest, e.org)] = e.sym
        return index

    def _index_corridor_edges(self, corridor: Corridor):
        """Indexes the edges of a single corridor square, for lookup of existing edges."""
        for e in corridor.edges:
            self.edges[(e.org, e.dest)] = e
            self.edges[(e.dest, e.org)] = e.sym

    def _is_corridor(self, square: PointInt) -> bool:
        corridor = self._get_square(square)
        if corridor is not None and isinstance(corridor, Corridor):
            return True
        return False

    def _is_room(self, square: PointInt):
        room = self._get_square(square)
        if room is not None and isinstance(room, Room):
            return True
        return False


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


class Path:
    """Class representing a path in the labyrinth.

    Implemented as a linked list.

    Attributes:
        `f_length`: approximate total length of the path, current length + heuristic
        `g_length`: current length of the path
        `current`: current coordinate of the square
        `direction`: direction of current square relative to the previous square
        `path`: previous square
    """
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
    """Class implementing A* pathfinding between two labyrinth squares.
    """
    def __init__(self, labyrinth: Labyrinth):
        self.labyrinth: Labyrinth = labyrinth

    def find_path(self, start: PointInt, end: PointInt) -> Path | None:
        """"
        A* search.

        Args:
            `start`: coordinates of start square
            `end`: coordinates of end square
        
        Returns:
            shortest path connecting the two squares
        """
        first = Path(self._heuristic(start, end), 0, start, None, None)
        size = len(self.labyrinth.squares)
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
        """Expands a node.
        
        Existing corridor squares are weighed less.
        """
        if self._closed(closed_list, current_path.current):
            return
        self._close(closed_list, current_path.current)
        neighbors = self._neighbors(current_path.current)
        for neighbor, direction in neighbors:
            if self._closed(closed_list, neighbor):
                continue
            weight = 0.5 if self.labyrinth._is_corridor(neighbor) else 1
            c_direction = current_path.direction
            if c_direction is None or direction == c_direction:
                penalty = 0
            else:
                penalty = 0.2
            g = current_path.g_length + weight + penalty
            h = self._heuristic(neighbor, end)
            path = Path(g + h, g, neighbor, direction, current_path)
            hq.heappush(open_list, path)

    def _found(self, path: Path, end: PointInt):
        room = self.labyrinth._get_square(path.current)
        return room is not None and room.center == end

    def _heuristic(self, a: PointInt, b: PointInt):
        """Returns the Manhattan distance between two squares."""
        # return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        return 0.5 * (abs(a[0] - b[0]) + abs(a[1] - b[1]))
        # return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    def _neighbors(self, square: PointInt) -> list[tuple[PointInt, Direction]]:
        """Returns the four neighboring squares."""
        squares: list[tuple[PointInt, Direction]] = []
        if square[1] + 1 < len(self.labyrinth.squares):
            north = (square[0], square[1] + 1)
            squares.append((north, Direction.NORTH))
        if square[1] > 0 and square[1] - 1 < len(self.labyrinth.squares):
            south = (square[0], square[1] - 1)
            squares.append((south, Direction.SOUTH))
        if square[0] > 0 and square[0] - 1 < len(self.labyrinth.squares[0]):
            west = (square[0] - 1, square[1])
            squares.append((west, Direction.WEST))
        if square[0] + 1 < len(self.labyrinth.squares[0]):
            east = (square[0] + 1, square[1])
            squares.append((east, Direction.EAST))
        return squares


class RoomGenerator:
    def __init__(
        self,
        num_rooms: int,
        min_dim: int,
        max_dim: int,
        gap: int,
        shape: str,
        seed: int,
    ):
        self.num_rooms: int = num_rooms
        self.min_dim: int = min_dim
        self.max_dim: int = max_dim
        self.gap: int = gap
        self.shape: str = shape
        self.seed: int = seed

        self.size: float = max_dim
        self.max_tries: int = 10000

    def _generate_rooms(self):
        size = floor(self.size)
        rooms: list[Room] = []
        room_squares: list[list[Rectangle | None]] = [
            [None] * (size) for _ in range(size)
        ]
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
            height = random.randint(max(self.min_dim, width // 2 + 1), width)
            if random.random() > 0.5:
                width, height = height, width
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

    def _generate_point(self, size: int) -> tuple[int, int]:
        max_pos = size - self.max_dim
        if self.shape == "circle":
            return point_in_circle(max_pos)
        if self.shape == "square":
            return point_in_square(max_pos)
        raise ValueError("Bad shape")

    def _create_and_occupy_room(
        self,
        occupied: list[list[bool]],
        room_squares: list[list[Rectangle | None]],
        size: int,
        corner: PointInt,
        width: int,
        height: int,
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

    def _room_fits(
        self, occupied: list[list[bool]], corner: PointInt, width: int, height: int
    ):
        for w in range(-self.gap, width):
            for h in range(-self.gap, height):
                if occupied[corner[1] + h][corner[0] + w]:
                    return False
        return True

    def _invalid_room(
        self, corner: PointInt, size: int, width: int, height: int
    ) -> bool:
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
    mid = max_pos // 2
    mid2 = mid * mid
    while True:
        x = random.randint(0, max_pos)
        y = random.randint(0, max_pos)
        if (x - mid) ** 2 + (y - mid) ** 2 <= mid2:
            break
    return (x, y)


def point_in_square(max_pos: int):
    x = random.randint(0, max_pos)
    y = random.randint(0, max_pos)
    return (x, y)

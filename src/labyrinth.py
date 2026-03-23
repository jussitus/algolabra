import random
from math import sqrt, floor
import heapq as hq
from delaunay import PlanarGraph
from edge import Edge, make_quad_edge, splice
from point import Point

# WIP


class Rectangle:
    def __init__(self, corner, width=1, height=1):
        self.width = width
        self.height = height
        self.corner = corner
        self.center = (corner[0] + width // 2, corner[1] + height // 2)
        self.edges, self.corner_edge = self.create()

    def create(self):
        def add_side(edges, current, length, displacement):
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

        edges = []
        corner_edge = make_quad_edge(self.corner, (self.corner[0] + 1, self.corner[1]))
        edges.append(corner_edge)
        top = add_side(edges, corner_edge, self.width - 1, (1, 0))
        right = add_side(edges, top, self.height, (0, 1))
        bottom = add_side(edges, right, self.width, (-1, 0))
        left = add_side(edges, bottom, self.height, (0, -1))
        splice(left.sym, corner_edge)
        return edges, corner_edge


class Room(Rectangle):
    def __init__(self, *args):
        super().__init__(*args)


class Corridor(Rectangle):
    def __init__(self, *args):
        super().__init__(*args)


class Labyrinth:
    def __init__(self, n_rooms, seed=0):
        self.n_rooms = n_rooms
        self.seed = seed
        self.max_dim = 8  # max(5, floor(sqrt(max_rooms)))
        self.min_dim = 2  # max(2, self.max_dim // 3)
        self.gap = 1
        self.modifier = 1
        self.max_tries = 1000
        self.rooms, self.room_squares, self.room_centers = self.generate_rooms(n_rooms)
        self.corridor_squares = [
            [None] * len(self.room_squares) for _ in range(len(self.room_squares))
        ]
        self.corridors = self.create_corridors()

    def generate_rooms(self, n):
        rooms = []
        room_centers = []
        total = floor(self.max_dim * self.modifier)
        occupied = [[False] * (total) for _ in (total)]
        room_squares = [[None] * (total) for _ in range(total)]
        tries = 0
        if self.seed:
            random.seed(self.seed)
        while len(rooms) < n:
            if tries == self.max_tries:
                # print(f"Could not fit any more rooms in {self.max_tries} tries for total={total}. Trying more sparse layout...")
                self.modifier *= 1.05
                return self.generate_rooms(self.n_rooms)
            valid = True
            corner = point_in_circle(total - self.max_dim)
            width = random.randint(self.min_dim, self.max_dim)
            height = random.randint(self.min_dim, self.max_dim)
            if (
                corner[0] + width + self.gap > len(room_squares[0])
                or corner[1] + height + self.gap > len(room_squares)
                or corner[0] - self.gap > len(room_squares[0])
                or corner[1] - self.gap > len(room_squares)
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
                        room_squares[corner[1] + h][corner[0] + w] = room
            rooms.append(room)
            room_centers.append(room.center)
        return rooms, room_squares, room_centers

    def create_corridors(self):
        def distance(a, b):
            if self.get_room_of_square(a) is self.get_room_of_square(b):
                return -10000
            # return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

        def neighbors(square):
            squares = []
            if square[1] + 1 < len(self.room_squares):
                up = (square[0], square[1] + 1)
                squares.append(up)
            if square[1] - 1 < len(self.room_squares):
                down = (square[0], square[1] - 1)
                squares.append(down)
            if square[0] - 1 < len(self.room_squares[0]):
                left = (square[0] - 1, square[1])
                squares.append(left)
            if square[0] + 1 < len(self.room_squares[0]):
                right = (square[0] + 1, square[1])
                squares.append(right)
            return squares

        def find_path(start, end):
            heap = []
            visited = [
                [False] * len(self.room_squares) for _ in range(len(self.room_squares))
            ]
            first = (distance(start, goal), start, None)
            visited[first[1][1]][first[1][0]] = True
            hq.heappush(heap, first)
            while True:
                current = hq.heappop(heap)
                for neighbor in neighbors(current[1]):
                    # print(f"width={len(self.room_squares[0])}, height={len(self.room_squares)}, current={neighbor}")
                    room_in_square = self.room_squares[neighbor[1]][neighbor[0]]
                    if room_in_square is not None and (room_in_square.center == goal):
                        return current
                    if not visited[neighbor[1]][neighbor[0]]:
                        if not self.corridor_squares[neighbor[1]][
                            neighbor[0]
                        ]:  # and not room_in_square
                            visited[neighbor[1]][neighbor[0]] = True
                            hq.heappush(
                                heap,
                                (
                                    distance(neighbor, goal) + current[0],
                                    neighbor,
                                    current,
                                ),
                            )
                        else:
                            visited[neighbor[1]][neighbor[0]] = True
                            hq.heappush(heap, (current[0], neighbor, current))

        connections = self.connect_rooms(self.room_centers)
        # print(self.room_centers)
        corridors = []
        for edge in connections:
            r1 = self.get_room_of_square(edge.org)
            r2 = self.get_room_of_square(edge.dest)
            start = r1.center
            goal = r2.center
            path = find_path(start, goal)
            prev = path
            while prev[2] is not None:
                if self.get_room_of_square(prev[1]) is None:
                    if not self.corridor_squares[prev[1][1]][prev[1][0]]:
                        self.corridor_squares[prev[1][1]][prev[1][0]] = True
                        corridor = Rectangle(prev[1])
                        corridors.append(corridor)
                prev = prev[2]
        return corridors

    def get_room_of_square(self, square: Point):
        return self.room_squares[square[1]][square[0]]  # type: ignore

    def connect_rooms(self, room_centers):
        d = PlanarGraph(room_centers)
        d.run()
        return d.mst_delaunay


def point_in_circle(width):
    mid_x = width // 2
    mid_y = width // 2
    while True:
        x = random.randint(0, width)
        y = random.randint(0, width)
        if sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2) <= max(mid_x, mid_y):
            point = (x, y)
            break
    return point

from random import randint, seed
from math import sqrt, floor
import heapq as hq
from tqdm import tqdm
from delaunay import PlanarGraph
from point import Point

# REDO THIS


class Room:
    def __init__(self, corner, width, height):
        self.corner_upper_left: Point = corner
        self.corner_lower_left = (corner[0], corner[1] + height)
        self.corner_upper_right = (corner[0] + width, corner[1])
        self.corner_lower_right = (corner[0] + width, corner[1] + height)
        self.width = width
        self.height = height
        self.center = (corner[0] + width // 2, corner[1] + height // 2)
        self.connected = False


class Labyrinth:
    def __init__(self, max_rooms):
        self.max_rooms = max_rooms
        self.max_width = 5  # max(5, floor(sqrt(max_rooms)))
        self.max_height = 5  # max(5, floor(sqrt(max_rooms)))
        self.min_width = max(2, self.max_width // 3)
        self.min_height = max(2, self.max_height // 3)
        self.gap = 2
        self.sparsity = 0.5 * (self.max_width) / max_rooms
        self.max_tries = 100
        rooms, room_squares, room_centers = self.generate_rooms(max_rooms)
        self.rooms: list[Room] = rooms
        self.room_squares = room_squares
        self.room_centers = room_centers
        self.corridor_squares = [
            [False] * len(self.room_squares) for _ in range(len(self.room_squares))
        ]
        self.connections = self.connect_rooms(self.room_centers)
        self.create_corridors()

    def get_room_of_square(self, square: Point):
        return self.room_squares[square[1]][square[0]]  # type: ignore

    def generate_rooms(self, n):
        rooms = []
        room_centers = []
        gap = self.gap + 1
        total_x = floor(n * self.max_width * self.sparsity)
        total_y = floor(n * self.max_width * self.sparsity)
        occupied = [[False] * (total_x + gap) for _ in range(total_y + gap)]
        room_squares = [[None] * (total_x + gap) for _ in range(total_y + gap)]
        tries = 0
        seed(42)
        while len(rooms) < n:
            if tries == self.max_tries:
                # print(f"Could not fit any more rooms in {self.max_tries} tries. Trying more sparse layout...")
                self.sparsity *= 1.05
                return self.generate_rooms(self.max_rooms)
            valid = True
            corner = point_in_circle(
                total_x - self.max_width - 1, total_y - self.max_height - 1
            )
            width = randint(self.min_width - 1, self.max_width - 1)
            height = randint(self.min_height - 1, self.max_height - 1)
            for w in range(width + gap):
                for h in range(height + gap):
                    if occupied[corner[1] + h][corner[0] + w]:
                        valid = False
                        break
            if not valid:
                tries += 1
                continue
            tries = 0
            # print(f"creating room {n}: corner={corner}, width={width}, height={height}")
            room = Room(corner, width, height)
            for w in range(width + gap):
                for h in range(height + gap):
                    occupied[corner[1] + h][corner[0] + w] = True
                    if w <= width and h <= height:
                        room_squares[corner[1] + h][corner[0] + w] = room
            rooms.append(room)
            room_centers.append(room.center)
        return rooms, room_squares, room_centers

    def connect_rooms(self, room_centers):
        d = PlanarGraph(room_centers)
        d.run()
        return d.mst_delaunay

    def create_corridors(self):
        def manhattan(a, b):
            # return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
            # return abs(a[0] - b[0]) + abs(a[1] - b[1])
            # return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

        def neighbors(square):
            squares = []
            i = 1
            if square[1] + i < len(self.room_squares):
                up = (square[0], square[1] + 1)
                squares.append(up)
            if square[1] - i < len(self.room_squares):
                down = (square[0], square[1] - 1)
                squares.append(down)
            if square[0] - i < len(self.room_squares[0]):
                left = (square[0] - 1, square[1])
                squares.append(left)
            if square[0] + i < len(self.room_squares[0]):
                right = (square[0] + 1, square[1])
                squares.append(right)
            return squares

        def find_path(start, end):
            heap = []
            visited = [
                [False] * len(self.room_squares) for _ in range(len(self.room_squares))
            ]
            first = (manhattan(start, goal), start, None)
            visited[first[1][1]][first[1][0]] = True
            hq.heappush(heap, first)
            while True:
                current = hq.heappop(heap)
                # print(current)
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
                            # hq.heappush(heap, (manhattan(neighbor,goal), neighbor, current))
                            hq.heappush(
                                heap,
                                (
                                    manhattan(neighbor, goal) + current[0],
                                    neighbor,
                                    current,
                                ),
                            )
                        else:
                            visited[neighbor[1]][neighbor[0]] = True
                            hq.heappush(heap, (current[0], neighbor, current))

        for edge in tqdm(self.connections):
            r1 = self.get_room_of_square(edge.org)
            r2 = self.get_room_of_square(edge.dest)
            start = r1.center
            goal = r2.center
            path = find_path(start, goal)
            prev = path
            while prev[2] is not None:
                if self.get_room_of_square(prev[1]) is None:
                    self.corridor_squares[prev[1][1]][prev[1][0]] = True
                prev = prev[2]


def point_in_circle(max_x: int, max_y: int):
    mid_x = max_x // 2
    mid_y = max_y // 2
    while True:
        x = randint(0, max_x)
        y = randint(0, max_y)
        if sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2) <= max(mid_x, mid_y):
            point = (x, y)
            break
    return point

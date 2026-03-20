from random import randint, seed
from math import sqrt, floor


class Room:
    def __init__(self, corner, width, height):
        self.corner_upper_left = corner
        self.corner_lower_left = (corner[0], corner[1] + height)
        self.corner_upper_right = (corner[0] + width, corner[1])
        self.corner_lower_right = (corner[0] + width, corner[1] + height)
        self.width = width
        self.height = height
        self.center = (corner[0] + width // 2, corner[1] + height // 2)


class Labyrinth:
    def __init__(self, max_rooms):
        self.corridor_squares = []
        self.max_width = max(5, floor(sqrt(max_rooms)))
        self.max_height = max(5, floor(sqrt(max_rooms)))
        self.min_width = max(2, self.max_width // 3)
        self.min_height = max(2, self.max_height // 3)
        self.gap = 1
        self.sparsity = 3.5 * (self.max_width) / max_rooms
        self.max_tries = max_rooms**2
        self.rooms, self.room_squares, self.room_centers = self.generate_rooms(
            max_rooms
        )

    def generate_rooms(self, n):
        print(f"mw: {self.max_width}, mh: {self.max_height}")
        rooms = []
        room_centers = []
        gap = self.gap + 1
        total_x = floor(n * self.max_width * self.sparsity)
        total_y = floor(n * self.max_width * self.sparsity)
        occupied = [[False] * (total_x + gap) for _ in range(total_y + gap)]
        room_squares = [[None] * (total_x + gap) for _ in range(total_y + gap)]
        tries = 0
        while len(rooms) < n:
            if tries == self.max_tries:
                print(f"Could not fit any more rooms in {self.max_tries} tries")
                break
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
                # print(f"Invalid: {n}")
                tries += 1
                continue
            tries = 0
            # print(f"creating room {n}: corner={corner}, width={width}, height={height}")
            room = Room(corner, width + 1, height + 1)
            for w in range(width + gap):
                for h in range(height + gap):
                    occupied[corner[1] + h][corner[0] + w] = True
                    room_squares[corner[1] + h][corner[0] + w] = room
            rooms.append(room)
            room_centers.append(room.center)
            # print(f"n: {n}, rooms: {len(rooms)}")
        return rooms, room_squares, room_centers


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

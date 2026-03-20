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
    def __init__(self, n_rooms):
        self.corridor_squares = []
        self.max_width = max(5, floor(sqrt(n_rooms)))
        self.max_height = max(5, floor(sqrt(n_rooms)))
        self.gap = 1
        self.min_width = max(2, self.max_width // 2)
        self.min_height = max(2, self.max_height // 2)
        self.sparsity = (self.max_width + self.gap) / n_rooms
        self.rooms, self.room_squares, self.room_centers = self.generate_rooms(n_rooms)

    def generate_rooms(self, n):
        print(f"mw: {self.max_width}, mh: {self.max_height}")
        rooms = []
        room_centers = []
        gap = self.gap + 1
        total_x = floor(n * self.max_width * self.sparsity)
        total_y = floor(n * self.max_width * self.sparsity)
        occupied = [[False] * (total_x + gap) for _ in range(total_y + gap)]
        room_squares = [[None] * (total_x + gap) for _ in range(total_y + gap)]
        while len(rooms) < n:
            valid = True
            corner = (
                randint(0, total_x - self.max_width - 1),
                randint(0, total_y - self.max_height - 1),
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
                continue
            print(f"creating room {n}: corner={corner}, width={width}, height={height}")
            room = Room(corner, width + 1, height + 1)
            for w in range(width + gap):
                for h in range(height + gap):
                    occupied[corner[1] + h][corner[0] + w] = True
                    room_squares[corner[1] + h][corner[0] + w] = room
            rooms.append(room)
            room_centers.append(room.center)
            print(f"n: {n}, rooms: {len(rooms)}")
        return rooms, room_squares, room_centers

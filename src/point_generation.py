import random
from math import floor, sqrt


# bad, fix/remove
def points_spread(n: int, max_x: int, max_y: int, seed: int):
    if seed != -1:
        random.seed(seed)
    s = set()
    base = floor(sqrt(n))
    gap_x = max_x // base
    gap_y = max_y // base
    offset_x = gap_x // 2
    offset_y = gap_y // 2
    for i in range(base):
        for k in range(0, base):
            x = i * gap_x + random.randint(0, offset_x)
            y = k * gap_y + random.randint(0, offset_y)
            s.add((x, y))
    return sorted(list(s))


def points_random(n: int, max_x: int, max_y: int, seed: int):
    if seed != -1:
        random.seed(seed)
    s = set()
    while len(s) < n:
        s.add(
            (
                random.randint(0, max_x),
                random.randint(0, max_y),
            )
        )
    return sorted(list(s))


def points_circular(n: int, max_x: int, max_y: int, seed: int):
    if seed != -1:
        random.seed(seed)
    s = set()
    mid_x = max_x // 2
    mid_y = max_y // 2
    while len(s) < n:
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        if sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2) <= max(mid_x, mid_y):
            s.add((x, y))
    return sorted(list(s))

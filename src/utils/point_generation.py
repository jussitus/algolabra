import random
from math import sqrt


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


def points_circular_unit(n: int, max_x: int, max_y: int, seed: int):
    if seed != -1:
        random.seed(seed)
    s = set()
    mid_x = max_x // 2 / max_x
    mid_y = max_y // 2 / max_y
    while len(s) < n:
        x = random.random()
        y = random.random()
        if sqrt((x - mid_x) ** 2 + (y - mid_y) ** 2) <= max(mid_x, mid_y):
            s.add((x, y))
    return sorted(list(s))

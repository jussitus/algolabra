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
    s = [(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(n)]
    return sorted(s)

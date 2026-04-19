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

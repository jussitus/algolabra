import logging
import time
from functools import wraps


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("labyrinth")


def timer(level=logging.DEBUG):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            res = func(*args, **kwargs)
            end = time.perf_counter()
            logger.log(level, f"{func.__name__} took {end - start:.4f} seconds")
            return res

        return wrapper

    return decorator


def log_after_state(level=logging.DEBUG):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs,):
            res = func(self, *args, **kwargs)
            logger.log(level, f"{self}")
            return res
        return wrapper
    return decorator
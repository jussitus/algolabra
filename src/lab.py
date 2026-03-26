# pyright: basic
import logging

logging.basicConfig(level=logging.WARNING)

from log_utils import logger

logger.setLevel(logging.DEBUG)

from argparse import ArgumentParser
from graphics import EdgeDrawer
from labyrinth import Labyrinth


def parse_arguments():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "-n",
        "--num-rooms",
        required=True,
        type=int,
        help="number of rooms in the labyrinth",
    )
    parser.add_argument("-s", "--seed", default=-1, type=int, help="random seed")
    parser.add_argument(
        "-Md", "--max-dim", default=10, type=int, help="maximum width/height of rooms"
    )
    parser.add_argument(
        "-md", "--min-dim", default=2, type=int, help="minimum width/height of rooms"
    )
    return parser.parse_args()


def main(args):
    num_rooms = args.num_rooms
    seed = args.seed
    max_dim = args.max_dim
    min_dim = args.min_dim
    lab = Labyrinth(num_rooms, seed, max_dim, min_dim)
    rectangles = []
    for room in lab.rooms:
        room_edges = [e.org for e in room.edges]
        room_edges.append(room.edges[-1].dest)
        rectangles.append(room_edges)

    for room in lab.corridors:
        room_edges = [e.org for e in room.edges]
        room_edges.append(room.edges[-1].dest)
        rectangles.append(room_edges)

    edge_drawer = EdgeDrawer()
    edge_drawer.add_edges(rectangles, colors="black", linewidths=1.5)
    edge_drawer.show()


if __name__ == "__main__":
    main(parse_arguments())

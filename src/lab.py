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
    _ = parser.add_argument(
        "-n",
        "--num-rooms",
        required=True,
        type=int,
        help="number of rooms in the labyrinth",
    )
    return parser.parse_args()


def main(args):
    num_rooms = args.num_rooms
    lab = Labyrinth(num_rooms)
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

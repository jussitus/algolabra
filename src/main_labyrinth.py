# pyright: basic
import logging

logging.basicConfig(level=logging.WARNING)

from utils.log_utils import logger

logger.setLevel(logging.DEBUG)

from argparse import ArgumentParser
from graphics import Drawer
from labyrinth import Labyrinth, Room


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
    parser.add_argument("-g", "--gap", default=1, type=int, help="gap between rooms")
    parser.add_argument(
        "-sh",
        "--shape",
        default="circle",
        type=str,
        choices=["circle", "square"],
        help="shape of the labyrinth",
    )
    parser.add_argument(
        "-c",
        "--cycle-score",
        default=0.2,
        type=float,
        help="percentage of cycles added to the labyrinth, 0-1.0",
    )
    return parser.parse_args()


def main(args):
    num_rooms = args.num_rooms
    seed = args.seed
    max_dim = args.max_dim
    min_dim = args.min_dim
    gap = args.gap
    shape = args.shape
    cycle_score = args.cycle_score
    lab = Labyrinth(num_rooms, seed, max_dim, min_dim, gap, shape, cycle_score)

    walls = []
    shared = []
    rectangles = lab.rooms + lab.corridors
    for rec in rectangles:
        for edge in rec.edges:
            if edge.data != "shared":
                walls.append([edge.org, edge.dest])
            else:
                shared.append([edge.org, edge.dest])

    drawer = Drawer()
    drawer.add_edges(walls, colors="black", linewidths=1.5)
    drawer.add_edges(shared, colors="black", linewidths=1.5, alpha=0.2)
    drawer.show()


if __name__ == "__main__":
    main(parse_arguments())

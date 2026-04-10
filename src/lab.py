# pyright: basic
import logging

logging.basicConfig(level=logging.WARNING)

from utils.log_utils import logger

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
    parser.add_argument(
        "-g", "--gap", default=1, type=int, help="gap between rooms"
    )
    return parser.parse_args()


def main(args):
    num_rooms = args.num_rooms
    seed = args.seed
    max_dim = args.max_dim
    min_dim = args.min_dim
    gap = args.gap
    lab = Labyrinth(num_rooms, seed, max_dim, min_dim, gap)

    
    first = lab.rooms[0].edges[0]
    lines = [[first.org, first.dest]]
    current = first.lnext
    lines.append([current.org, current.dest])
    while True:
        if current is not current.lnext and current is not first:
            current = current.lnext
            print(current)
            if current.data != "shared":
                lines.append([current.org, current.dest])
        else:
            break
    # lines = []
    # rectangles = lab.rooms + lab.corridors
    # for rec in rectangles:
    #     for edge in rec.edges:
    #         if edge.data != "shared":
    #             lines.append([edge.org, edge.dest])


    edge_drawer = EdgeDrawer()
    edge_drawer.add_edges(lines, colors="black", linewidths=1.5)
    edge_drawer.show()


if __name__ == "__main__":
    main(parse_arguments())

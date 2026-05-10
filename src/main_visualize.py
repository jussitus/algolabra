# pyright: basic
import logging

logging.basicConfig(level=logging.WARNING)

from utils.log_utils import logger
from utils.point_generation import points_random

logger.setLevel(logging.DEBUG)

from argparse import ArgumentParser
from graphics import Drawer
from planar_graph import PlanarGraph


def parse_arguments():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "-n",
        required=True,
        type=int,
        help="number of points",
    )
    parser.add_argument("-s", "--seed", default=-1, type=int, help="random seed")
    parser.add_argument(
        "-d", "--delaunay", action="store_true", help="draw Delaunay triangulation"
    )
    parser.add_argument(
        "-v", "--voronoi", action="store_true", help="draw Voronoi diagram"
    )
    parser.add_argument(
        "-c", "--circumcircles", action="store_true", help="draw circumcircles"
    )
    return parser.parse_args()


def main(args):
    n = args.n
    s = args.seed
    d = args.delaunay
    v = args.voronoi
    c = args.circumcircles
    points = points_random(n, n, n, s)
    planar_graph = PlanarGraph(points)
    planar_graph.run()

    edges_d = []
    edges_v = []
    circles = []
    for e in planar_graph.delaunay:
        edges_d.append((e.org, e.dest))
    for e in planar_graph.voronoi:
        edges_v.append((e.org, e.dest))
        if e.radius is not None:
            circles.append(((e.org), e.radius))

    drawer = Drawer()
    if d:
        drawer.add_edges(edges_d, colors="black", linewidths=1)
    if v:
        drawer.add_edges(edges_v, colors="blue", linewidths=1, alpha=0.5)
    if c:
        drawer.add_circles(
            circles, edgecolor="red", facecolor="none", linewidths=0.75, alpha=0.5
        )
    drawer.show()


if __name__ == "__main__":
    main(parse_arguments())

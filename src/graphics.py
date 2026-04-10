import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from point import Point


class EdgeDrawer:
    def __init__(
        self,
    ):
        self._fig, self._ax = plt.subplots()

    def add_edges(self, edges: list[tuple[Point]], **kwargs):
        lc: LineCollection = LineCollection(edges, **kwargs)
        self._ax.add_collection(lc)

    def show(self):
        self._ax.invert_yaxis()
        self._ax.axis("equal")
        self._ax.autoscale()
        plt.show()

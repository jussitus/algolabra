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
        _ = self._ax.add_collection(lc)

    def show(self):
        _ = self._ax.axis("equal")
        _ = self._ax.autoscale()
        _ = plt.show()

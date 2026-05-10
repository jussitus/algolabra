import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from point import Point


class Drawer:
    def __init__(
        self,
    ):
        self._fig, self._ax = plt.subplots()

    def add_edges(self, edges: list[tuple[Point]], **kwargs):
        lc: LineCollection = LineCollection(edges, **kwargs)
        self._ax.add_collection(lc)

    def add_circles(self, circles, **kwargs):
        cc = [Circle(o,r) for (o, r) in circles]
        pc = PatchCollection(cc, **kwargs)
        self._ax.add_collection(pc)
        
    def show(self):
        self._ax.invert_yaxis()
        self._ax.axis("equal")
        self._ax.autoscale()
        plt.show()
